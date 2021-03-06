from django.db import models
from django.conf import settings
import uuid
from itertools import chain
from django.utils import timezone as dj_timezone
import pytz
from datetime import datetime, date, time, timedelta
from django.utils import timezone

nth = {
    1: 'first',
    2: 'second',
    3: 'third',
    4: 'fourth',
    5: 'fifth',
}


class Goal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    timezone = models.TextField()

    text = models.TextField(max_length=1024)
    start = models.DateTimeField()

    active = models.BooleanField(default=False)
    lives = models.IntegerField(default=3)
    complete = models.BooleanField(default=False)

    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-start',)

    def __str__(self):
        return '%s (%s)' % (self.id, self.user.email)

    def create_step(self, text, start=None, commit=False):
        if start is not None and dj_timezone.is_naive(start):
            raise ValueError()

        if start is None:
            start = timezone.now()

        step = Step(goal=self, text=text, start=start)
        step.update_end()

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
        return nth[int(self.next_step_num)]

    @property
    def current_step(self):
        return self.steps.last()

    @property
    def step_emails(self):
        return list(chain.from_iterable(
            [step.emails.all() for step in self.steps.all()]))

    def step_email(self, name):
        for email in self.step_emails:
            if email.name == name:
                return email

        return None


class Step(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    goal = models.ForeignKey(Goal, related_name='steps',
                             on_delete=models.CASCADE)

    text = models.CharField(max_length=1024)
    start = models.DateTimeField()  # UTC
    end = models.DateTimeField()
    time_tracked = models.DateTimeField(blank=True, null=True)

    complete = models.BooleanField(default=False)
    comments = models.TextField(max_length=1024, blank=True)

    class Meta:
        ordering = ('start',)

    @staticmethod
    def create(goal: Goal, text: str):
        start = timezone.now()

        return Step.objects.create(
            goal=goal,
            text=text,
            start=start,
            end=Step.deadline(start, goal.timezone)
        )

    @staticmethod
    def deadline(start, tz):
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

    def update_end(self):
        self.end = Step.deadline(self.start, self.goal.timezone)

    def lose_life(self, now=None, commit=True):
        if now is None:
            now = timezone.now()

        tz = pytz.timezone(self.goal.timezone)

        self.goal.lives -= 1
        self.end = (now.astimezone(tz) + timedelta(days=1)) \
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
        return nth[self.number]

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
