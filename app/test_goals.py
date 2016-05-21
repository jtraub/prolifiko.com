from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid1
from datetime import timedelta
from unittest.mock import patch
from django.dispatch import Signal

from .models import Goal
from .views import goals as views


class GoalsTest(TestCase):
    fixtures = ['goals']

    def setUp(self):
        self.client = Client()
        self.client.login(username="test", password="test")

        self.user = User.objects.get(username="test")

    def test_new_no_text(self):
        response = self.client.post(reverse('app_goals_new'))

        self.assertEquals(400, response.status_code)

    @patch('app.views.goals.new_goal', spec=Signal)
    def test_new(self, new_goal):
        text = uuid1()
        response = self.client.post(reverse('app_goals_new'), data={
            'text': text
        }, follow=False)

        goal = Goal.objects.get(text=text)

        self.assertRedirects(response, reverse('app_steps_new',
                                               kwargs={'goal_id': goal.id}))

        self.assertIsNotNone(goal)
        self.assertEquals(self.user.id, goal.user.id)
        self.assertAlmostEquals(timezone.now(), goal.start,
                                delta=timedelta(seconds=3))
        self.assertEquals(goal.start + timedelta(days=5), goal.end)

        new_goal.send.assert_called_with(views.new, goal=goal)

    def test_new_form(self):
        response = self.client.get(reverse('app_goals_new'))

        self.assertEquals(200, response.status_code)
