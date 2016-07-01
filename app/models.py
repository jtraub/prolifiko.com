from django.db import models
from django.utils import timezone
from django.conf import settings
from django import forms
import uuid
from itertools import chain

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

    text = models.TextField(max_length=144)
    start = models.DateTimeField(default=timezone.now)

    active = models.BooleanField(default=False)
    lives = models.IntegerField(default=3)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return '%s (%s)' % (self.id, self.user.email)

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

    text = models.CharField(max_length=144)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()
    time_tracked = models.DateTimeField(blank=True, null=True)

    complete = models.BooleanField(default=False)
    comments = models.TextField(max_length=144, blank=True)

    class Meta:
        ordering = ('start',)

    @staticmethod
    def create(goal: Goal, text: str):
        start = timezone.now()
        end = start + settings.INACTIVE_DELTA

        return Step.objects.create(
            goal=goal,
            text=text,
            start=start,
            end=end
        )

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
