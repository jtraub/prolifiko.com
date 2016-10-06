from datetime import timedelta
from uuid import uuid1
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone
from app.models import Goal, Timezone, Step, Subscription
import django.test as django_test


def client(u: User=None, subscribed=True):
    if u is None:
        u = user(subscribed=subscribed)

    c = Client()
    c.login(username=u.username, password='test')

    return c


def user(email=None, tz=None, subscribed=True):
    if email is None:
        email = uuid1().hex + '@test.com'
    if tz is None:
        tz = 'Europe/London'

    u = User(email=email, username=email, password='test')
    u.set_password('test')
    u.save()

    Timezone.objects.create(user=u, name=tz)

    if subscribed:
        Subscription.objects.create(user=u, name='test')

    return u


def goal(u: User=None, *args, **kwargs):
    if u is None:
        u = user()

    kwargs.setdefault('type', Goal.TYPE_CUSTOM)
    kwargs.setdefault('name', 'Test Goal')
    kwargs.setdefault('description', 'A goal description')
    kwargs.setdefault('start', timezone.now())
    kwargs.setdefault('target', timezone.now().date() + timedelta(days=5))

    return Goal.objects.create(user=u, **kwargs)


def five_day_challenge(u: User=None, *args, **kwargs):
    kwargs['type'] = Goal.TYPE_FIVE_DAY
    return goal(u, **kwargs)


def step(g: Goal=None, tz=None, *args, **kwargs):
    if g is None:
        g = goal()
    if tz is None:
        tz = Timezone.objects.get(user=g.user).name

    kwargs.setdefault('name', 'Test Step')
    kwargs.setdefault('description', 'A step description')
    kwargs.setdefault('start', timezone.now())
    kwargs.setdefault('deadline', Step.midnight_deadline(kwargs['start'], tz))

    return Step.objects.create(goal=g, **kwargs)


class TestCase(django_test.TestCase):
    def setUp(self):
        self.user = user()

        self.client = Client()
        self.client.login(username=self.user.username, password='test')
