from datetime import timedelta
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone
from app.models import Goal, Timezone, Step
import django.test as django_test


def client(u: User):
    c = Client()
    c.login(username=u.username, password='test')

    return c


def user(email=None, tz=None):
    if email is None:
        email = 'test@test.com'
    if tz is None:
        tz = 'Europe/London'

    u = User.objects.create(email=email, username=email, password='test')
    Timezone.objects.create(user=user, name=tz)

    return u


def five_day_challenge(u: User=None, start=None):
    start = start if start is not None else timezone.now()

    return Goal.objects.create(user=u,
                               type='FIVE_DAY_CHALLENGE',
                               name='test',
                               description='test',
                               start=start)


def goal(u: User=None, *args, **kwargs):
    if u is None:
        u = user()

    kwargs.setdefault('name', 'Test Goal')
    kwargs.setdefault('description', 'A goal description')
    kwargs.setdefault('start', timezone.now())
    kwargs.setdefault('target', timezone.now().date() + timedelta(days=5))

    return Goal.objects.create(user=u, **kwargs)


def step(g: Goal, tz=None, *args, **kwargs):
    if tz is None:
        tz = 'Europe/London'

    start = timezone.now()

    return g.create_step(
        kwargs.get('name', 'Test Step'),
        kwargs.get('description', 'A step description'),
        kwargs.get('start', timezone.now()),
        kwargs.get('deadline', Step.midnight_deadline(start, tz)),
        commit=True
    )


class TestCase(django_test.TestCase):
    fixtures = ['users']

    def setUp(self):
        self.client = Client()
        self.client.login(username='test', password='test')

        self.user = User.objects.get(username='test')
