from uuid import uuid1
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone
from app.models import Goal, Timezone
import django.test as django_test


def client(user):
    client = Client()
    client.login(username=user.username, password='test')

    return client


def user(email, timezone):
    user = User.objects.create(email=email, username=email, password='test')
    Timezone.objects.create(user=user, name=timezone)

    return user


def five_day_challenge(user, start=None):
    start = start if start is not None else timezone.now()

    return Goal.objects.create(user=user,
                               type='FIVE_DAY_CHALLENGE',
                               name='test',
                               description='test',
                               start=start)


class TestCase(django_test.TestCase):
    fixtures = ['users']

    def setUp(self):
        self.client = Client()
        self.client.login(username='test', password='test')

        self.user = User.objects.get(username='test')
