from django.test import TestCase, Client, RequestFactory, override_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid1

from django.utils.timezone import now
from datetime import timedelta
from unittest.mock import patch
from django.dispatch import Signal

from app.models import Goal
from app.views import goals as views


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

        new_goal.send.assert_called_with('app.views.goals.new', goal=goal)

    @patch('app.views.goals.goal_complete', spec=Signal)
    def test_complete(self, goal_complete):
        goal = Goal.objects.filter(user=self.user).first()

        response = self.client.post(reverse('app_goals_complete',
                                            kwargs={'goal_id': goal.id}))

        self.assertContains(response, 'feedback')

        goal.refresh_from_db()

        self.assertTrue(goal.complete)

        goal_complete.send.assert_called_with(
            'app.views.goals.complete', goal=goal)

    def test_new_form(self):
        response = self.client.get(reverse('app_goals_new'))

        self.assertEquals(200, response.status_code)


@override_settings(DEBUG=True)
class LivesTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_0_lives_lost(self):
        user = User.objects.create(username='lives0', password='test')
        request = self.factory.post(reverse('app_goals_new'),
                                    data={'text': 'test'})
        request.user = user

        views.new(request)

        goal = Goal.objects.filter(user=user).first()
        self.assertEquals(3, goal.lives)

    def test_1_life_lost(self):
        user = User.objects.create(username='lives1', password='test',
                                   date_joined=now() - timedelta(hours=24))
        request = self.factory.post(reverse('app_goals_new'),
                                    data={'text': 'test'})
        request.user = user

        views.new(request)

        goal = Goal.objects.filter(user=user).first()
        self.assertEquals(2, goal.lives)

    def test_2_lives_lost(self):
        user = User.objects.create(username='lives1', password='test',
                                   date_joined=now() - timedelta(hours=48))

        request = self.factory.post(reverse('app_goals_new'),
                                    data={'text': 'test'})
        request.user = user

        views.new(request)

        goal = Goal.objects.filter(user=user).first()
        self.assertEquals(1, goal.lives)
