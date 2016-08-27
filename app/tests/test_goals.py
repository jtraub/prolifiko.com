from django.test import TestCase, Client, RequestFactory, override_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid1

from django.utils.timezone import now, pytz
from datetime import timedelta, datetime, time
from unittest.mock import patch
from django.dispatch import Signal

from app.models import Goal, Step
from app.views import goals as views


class GoalsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="test", password="test")

        self.user = User.objects.get(username="test")

    def test_new_form(self):
        response = self.client.get(reverse('app_goals_new'))

        self.assertEquals(200, response.status_code)
        self.assertTrue('timezones' in response.context)

    def test_new_form_redirects_to_existing_goal(self):
        goal = Goal.objects.create(user=self.user, text='test',
                                   timezone='Europe/London',
                                   start=timezone.now())

        response = self.client.get(reverse('app_goals_new'), follow=True)

        timeline_url = reverse('app_goals_timeline',
                               kwargs={'goal_id': goal.id})
        self.assertEquals(response.redirect_chain[0], (timeline_url, 302))

    def test_new_no_text(self):
        response = self.client.post(reverse('app_goals_new'), data={
            'first_step': 'step text',
            'timezone': 'Europe/London'
        })

        self.assertEquals(400, response.status_code)

    def test_new_no_first_step(self):
        response = self.client.post(reverse('app_goals_new'), data={
            'text': 'goal text',
            'timezone': 'Europe/London'
        })

        self.assertEquals(400, response.status_code)

    def test_new_no_timezone(self):
        response = self.client.post(reverse('app_goals_new'), data={
            'text': 'goal text',
            'first_step': 'step text'
        })

        self.assertEquals(400, response.status_code)

    @patch('app.views.goals.new_goal', spec=Signal)
    @patch('app.views.goals.new_step', spec=Signal)
    def test_new(self, new_step, new_goal):
        text = uuid1()
        response = self.client.post(reverse('app_goals_new'), data={
            'text': text,
            'first_step': 'step text',
            'timezone': 'Europe/London'
        }, follow=False)

        goal = Goal.objects.get(text=text)
        tz = pytz.timezone('Europe/London')

        self.assertEquals(len(goal.steps.all()), 1)

        self.assertRedirects(response, reverse('app_steps_start', kwargs={
            'goal_id': goal.id, 'step_id': goal.steps.first().id}))

        self.assertIsNotNone(goal)
        self.assertEquals(goal.lives, 3)
        self.assertEquals(self.user.id, goal.user.id)
        self.assertEquals(goal.timezone, 'Europe/London')
        self.assertAlmostEquals(goal.start, timezone.now(),
                                delta=timedelta(seconds=1))

        first_step = goal.steps.first()
        self.assertEquals(first_step.text, 'step text')
        self.assertEquals(first_step.start, goal.start)

        local_start = first_step.start.astimezone(tz)
        local_end = first_step.end.astimezone(tz)
        self.assertEquals(first_step.end, Step.deadline(first_step.start, tz))
        self.assertEquals((local_start + timedelta(days=2)).date(),
                          local_end.date())
        self.assertEquals(local_end.time(), time())

        new_goal.send.assert_called_with('app.views.goals.new',
                                         goal=goal)
        new_step.send.assert_called_with('app.views.goals.new',
                                         step=first_step)

    @patch('app.views.goals.goal_complete', spec=Signal)
    def test_complete(self, goal_complete):
        goal = Goal.objects.create(user=self.user, text='test',
                                   timezone='Europe/London',
                                   start=timezone.now())

        response = self.client.post(reverse('app_goals_complete',
                                            kwargs={'goal_id': goal.id}))

        self.assertContains(response, 'feedback')

        goal.refresh_from_db()

        self.assertTrue(goal.complete)

        goal_complete.send.assert_called_with(
            'app.views.goals.complete', goal=goal)
