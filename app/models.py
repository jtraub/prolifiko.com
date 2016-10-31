from django.db import models
from django.conf import settings
import uuid
from itertools import chain
from django.utils import timezone as dj_timezone
import pytz
from datetime import timedelta
from django.utils import timezone
import inflect
inflect_engine = inflect.engine()


class Goal(models.Model):
    TYPE_FIVE_DAY = 'FIVE_DAY_CHALLENGE'
    TYPE_CUSTOM = 'CUSTOM'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    type = models.CharField(max_length=256, choices=((name, name) for name in (
        'FIVE_DAY_CHALLENGE',
        'CUSTOM',
    )))

    name = models.TextField(max_length=140)
    description = models.TextField(max_length=1024, blank=True)

    start = models.DateTimeField()
    target = models.DateField()

    active = models.BooleanField(default=False)
    lives = models.IntegerField(default=3)
    complete = models.BooleanField(default=False)

    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-start',)

    def __str__(self):
        return '%s (%s)' % (self.id, self.user.email)

    def create_step(self, name, description,
                    start, deadline,
                    commit=False):
        if start is not None and dj_timezone.is_naive(start):
            raise ValueError()

        if start is None:
            start = timezone.now()

        step = Step(goal=self,
                    name=name, description=description,
                    start=start, deadline=deadline)

        if commit:
            step.save()

            self.active = True
            self.save()

            self.refresh_from_db()

        return step

    def lose_life(self, commit=True):
        self.lives -= 1
        if commit:
            self.save()

    @property
    def next_step_num(self):
        return self.steps.count() + 1

    @property
    def next_step_nth(self):
        return inflect_engine.ordinal(self.next_step_num)

    @property
    def current_step(self):
        return self.steps.last()

    @property
    def step_emails(self):
        return list(chain.from_iterable(
            [step.emails.all() for step in self.steps.all()]))

    @property
    def is_five_day(self):
        return self.type == Goal.TYPE_FIVE_DAY

    def step_email(self, name):
        for email in self.step_emails:
            if email.name == name:
                return email

        return None


class Step(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    goal = models.ForeignKey(Goal, related_name='steps',
                             on_delete=models.CASCADE)

    name = models.TextField(max_length=140)
    description = models.TextField(max_length=1024, blank=True)

    start = models.DateTimeField()
    deadline = models.DateTimeField()

    time_tracked = models.DateTimeField(blank=True, null=True)

    complete = models.BooleanField(default=False)
    comments = models.TextField(max_length=1024, blank=True)

    class Meta:
        ordering = ('start',)

    @staticmethod
    def midnight_deadline(start, tz):
        if dj_timezone.is_naive(start):
            raise ValueError()

        if isinstance(tz, str):
            tz = pytz.timezone(tz)

        # - Convert UTC start time to goal timezone
        # - Update date and time to local midnight after next
        # - Convert back to UTC
        return (start.astimezone(tz) + timedelta(days=2)) \
            .replace(hour=0, minute=0, second=0, microsecond=0) \
            .astimezone(pytz.utc)

    def update_deadline(self):
        self.deadline = Step.midnight_deadline(self.start, self.goal.timezone)

    def lose_life(self, now=None, commit=True):
        if now is None:
            now = timezone.now()

        tz = pytz.timezone(Timezone.objects.get(user=self.goal.user).name)

        self.goal.lives -= 1
        self.deadline = (now.astimezone(tz) + timedelta(days=1)) \
            .replace(hour=0, minute=0, second=0, microsecond=0) \
            .astimezone(pytz.utc)

        if commit:
            self.goal.save()
            self.save()

    @property
    def number(self):
        if not hasattr(self, '_number'):
            self._number = list(self.goal.steps.all()).index(self) + 1

        return self._number

    @property
    def nth(self):
        return inflect_engine.ordinal(self.number)

    @property
    def user(self):
        return self.goal.user

    @property
    def in_progress(self):
        return self.end is None


class Email(models.Model):
    name = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='recipient')

    step = models.ForeignKey(Step,
                             blank=True,
                             null=True,
                             related_name='emails')

    TYPE_D = 'd'
    TYPE_DR = 'dr'
    TYPE_N = 'n'

    class Meta:
        ordering = ('sent',)

    @property
    def type(self):
        if self.name[:2] == 'dr':
            return Email.TYPE_DR

        if self.name[0] == 'n':
            return Email.TYPE_N

        return Email.TYPE_D


class Timezone(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    name = models.TextField()

    def __str__(self):
        return '%s (%s)' % (self.user.email, self.name)


class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    name = models.TextField()

    def __str__(self):
        return '%s (%s)' % (self.user.email, self.name)
