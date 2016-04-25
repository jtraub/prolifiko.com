from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from datetime import timedelta
from unittest.mock import patch

from .models import Goal, Step


class StepsTest(TestCase):
    fixtures = ['users', 'goals']

    def setUp(self):
        self.client = Client()
        self.client.login(username="test", password="test")

        self.user = User.objects.get(username="test")
        self.goal = Goal.objects.filter(user=self.user).first()

    def test_new_bad_goal(self):
        response = self.client.post(reverse('app_steps_new',
                                            kwargs={'goal_id': uuid4()}))

        self.assertEquals(404, response.status_code)

    def test_new_no_text(self):
        response = self.client.post(reverse('app_steps_new',
                                            kwargs={'goal_id': self.goal.id}))

        self.assertEquals(400, response.status_code)

    @patch('app.views.steps.keen')
    def test_new(self, keen):
        text = uuid4()
        response = self.client.post(
            reverse('app_steps_new', kwargs={'goal_id': self.goal.id}),
            data={'text': text},
            follow=False
        )

        step = Step.objects.get(text=text)

        self.assertRedirects(response, reverse('app_steps_start',
                                               kwargs={'goal_id': self.goal.id,
                                                       'step_id': step.id}))

        self.assertIsNotNone(step)
        self.assertEquals(self.goal.id, step.goal.id)
        self.assertAlmostEquals(timezone.now(), step.start,
                                delta=timedelta(seconds=3))
        self.assertEquals(step.start + timedelta(days=1), step.end)

        keen.add_event.assert_called_with('steps.new', {
            'id': step.id,
            'goal_id': step.goal.id,
            'user_id': self.user.id
        })

    def test_start_form(self):
        step = Step.objects.create(goal=self.goal, text=uuid4(),
                                   start=timezone.now(), end=timezone.now())

        response = self.client.get(reverse('app_steps_start', kwargs={
                'goal_id': step.goal.id, 'step_id': step.id}))

        self.assertEquals(200, response.status_code)

    def test_track_form(self):
        step = Step.objects.create(goal=self.goal, text=uuid4(),
                                   start=timezone.now(), end=timezone.now())

        response = self.client.get(reverse('app_steps_track', kwargs={
            'goal_id': step.goal.id, 'step_id': step.id}))

        self.assertEquals(200, response.status_code)

    @patch('app.views.steps.keen')
    def test_track_with_comments(self, keen):
        step = Step.objects.create(goal=self.goal, text=uuid4(),
                                   start=timezone.now(), end=timezone.now())

        response = self.client.post(
            reverse('app_steps_track', kwargs={
                'goal_id': step.goal.id, 'step_id': step.id}),
            data={'comments': 'foobar'},
            follow=False)

        self.assertRedirects(response, reverse('app_steps_complete',
                                               kwargs={'goal_id': self.goal.id,
                                                       'step_id': step.id}))

        step.refresh_from_db()
        self.assertEquals('foobar', step.comments)

        keen.add_event.assert_called_with('steps.track', {
            'id': step.id,
            'goal_id': step.goal.id,
            'user_id': self.user.id
        })

    @patch('app.views.steps.keen')
    def test_track_no_comments(self, keen):
        step = Step.objects.create(goal=self.goal, text=uuid4(),
                                   start=timezone.now(), end=timezone.now())

        response = self.client.post(
            reverse('app_steps_track', kwargs={
                'goal_id': step.goal.id, 'step_id': step.id}),
            follow=False)

        self.assertRedirects(response, reverse('app_steps_complete',
                                               kwargs={'goal_id': self.goal.id,
                                                       'step_id': step.id}))

        step.refresh_from_db()
        self.assertEquals('', step.comments)

        keen.add_event.assert_called_with('steps.track', {
            'id': step.id,
            'goal_id': step.goal.id,
            'user_id': self.user.id
        })

    def test_complete_form(self):
        step = Step.objects.create(goal=self.goal, text=uuid4(),
                                   start=timezone.now(), end=timezone.now())

        response = self.client.get(reverse('app_steps_complete', kwargs={
            'goal_id': step.goal.id, 'step_id': step.id}))

        self.assertEquals(200, response.status_code)

    @patch('app.views.steps.keen')
    def test_complete(self, keen):
        step = Step.objects.create(goal=self.goal, text=uuid4(),
                                   start=timezone.now(), end=timezone.now())

        response = self.client.post(
            reverse('app_steps_update', kwargs={
                'goal_id': step.goal.id, 'step_id': step.id}),
            follow=False)

        redirect = reverse('app_goals_timeline',
                           kwargs={'goal_id': self.goal.id})
        self.assertRedirects(response, redirect)

        step.refresh_from_db()
        self.assertEquals('', step.comments)

        keen.add_event.assert_called_with('steps.complete', {
            'id': step.id,
            'goal_id': step.goal.id,
            'user_id': self.user.id
        })
