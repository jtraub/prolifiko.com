from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid1
from datetime import timedelta

from .models import Goal


class GoalsTest(TestCase):
    fixtures = ['users', 'goals']

    def setUp(self):
        self.client = Client()
        self.client.login(username="test", password="test")

        self.user = User.objects.get(username="test")

    def test_new_no_text(self):
        response = self.client.post(reverse('app_goals_new'))

        self.assertEquals(400, response.status_code)

    def test_new(self):
        text = uuid1()
        response = self.client.post(reverse('app_goals_new'), {
            'text': text
        })

        self.assertRedirects(response, reverse('app_index'))

        goal = Goal.objects.get(text=text)
        self.assertIsNotNone(goal)
        self.assertEquals(self.user.id, goal.user.id)
        self.assertAlmostEquals(timezone.now(), goal.start,
                                delta=timedelta(seconds=3))
        self.assertEquals(goal.start + timedelta(days=5), goal.end)

    def test_new_first(self):
        self.client.login(username="empty", password="test")

        response = self.client.get(reverse('app_goals_new'))

        self.assertTrue(response.context['first'])
        self.assertContains(response, 'Create your first goal')

    def test_new_form(self):
        response = self.client.get(reverse('app_goals_new'))

        self.assertFalse(response.context['first'])
