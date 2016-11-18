from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils import timezone
from uuid import uuid4
from datetime import timedelta
from unittest.mock import patch
from django.dispatch import Signal
import pytz
from datetime import time

from app import fixtures
from app.models import Step


class StepsTest(TestCase):
    fixtures = ['goals']

    def setUp(self):
        self.user = fixtures.user(subscribed=False)
        self.goal = fixtures.five_day_challenge(self.user)

        self.client = fixtures.client(self.user)

    def test_new_bad_goal(self):
        response = self.client.post(reverse('new_step',
                                            kwargs={'goal_id': uuid4()}))

        self.assertEquals(404, response.status_code)

    def test_new_no_text(self):
        response = self.client.post(reverse('new_step',
                                            kwargs={'goal_id': self.goal.id}))

        self.assertEquals(400, response.status_code)

    @patch('app.views.steps.new_step', spec=Signal)
    def test_new_five_day(self, new_step_signal):
        goal = fixtures.five_day_challenge(self.user)

        name = uuid4()
        new_step_url = reverse('new_step', kwargs={'goal_id': goal.id})
        response = self.client.post(new_step_url, data={
            'step_name': name,
            'step_description': 'test',
        }, follow=False)

        step = Step.objects.get(name=name)

        self.assertRedirects(response, reverse('start_step', kwargs={
            'goal_id': goal.id, 'step_id': step.id}))

        self.assertIsNotNone(step)
        self.assertEquals(goal.id, step.goal.id)
        self.assertEquals(step.description, 'test')

        self.assertAlmostEquals(step.start, timezone.now(),
                                delta=timedelta(seconds=2))

        tz = pytz.timezone('Europe/London')
        local_start = step.start.astimezone(tz)
        local_deadline = step.deadline.astimezone(tz)
        self.assertEquals(step.deadline,
                          Step.midnight_deadline(step.start, tz))
        self.assertEquals((local_start + timedelta(days=2)).date(),
                          local_deadline.date())
        self.assertEquals(local_deadline.time(), time())

        new_step_signal.send.assert_called_with(
            'app.views.steps.new', step=step)

    @patch('app.views.steps.new_step', spec=Signal)
    def test_new_custom(self, new_step_signal):
        user = fixtures.user('custom_step@t.com')
        client = fixtures.client(user)

        goal = fixtures.goal(user)
        name = uuid4()

        new_step_url = reverse('new_step', kwargs={'goal_id': goal.id})
        response = client.post(new_step_url, data={
            'step_name': name,
            'step_description': 'test',
            'step_deadline': '2020-01-01',
        }, follow=False)

        step = Step.objects.get(name=name)

        self.assertRedirects(response, reverse('myprogress'))

        self.assertIsNotNone(step)
        self.assertEquals(goal.id, step.goal.id)
        self.assertEquals(step.description, 'test')

        tz = pytz.timezone('Europe/London')
        self.assertAlmostEquals(step.start, timezone.now(),
                                delta=timedelta(seconds=2))
        local_deadline = step.deadline.astimezone(tz)
        self.assertEquals(step.deadline, local_deadline)

        new_step_signal.send.assert_called_with(
            'app.views.steps.new', step=step)

    def test_start_five_day(self):
        goal = fixtures.five_day_challenge(self.user)
        step = fixtures.step(goal)

        response = self.client.get(reverse('start_step', kwargs={
                'goal_id': step.goal.id, 'step_id': step.id}))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.templates[0].name,
                          'steps/start_five_day.html')

    def test_track_form(self):
        step = fixtures.step(self.goal)

        response = self.client.get(reverse('complete_step', kwargs={
            'goal_id': step.goal.id, 'step_id': step.id}))

        self.assertEquals(200, response.status_code)

    @patch('app.views.steps.step_complete', spec=Signal)
    def test_track_with_comments(self, step_complete_signal):
        step = fixtures.step(self.goal)

        response = self.client.post(
            reverse('complete_step', kwargs={
                'goal_id': step.goal.id, 'step_id': step.id}),
            data={'comments': 'foobar'},
            follow=False)

        self.assertRedirects(response,
                             reverse('new_step',
                                     kwargs={'goal_id': self.goal.id}))

        step.refresh_from_db()
        self.assertEquals('foobar', step.comments)

        step_complete_signal.send.assert_called_with(
            'app.views.steps.track', step=step)

    @patch('app.views.steps.step_complete', spec=Signal)
    def test_track_no_comments(self, step_complete_signal):
        step = fixtures.step(self.goal)

        response = self.client.post(
            reverse('complete_step', kwargs={
                'goal_id': step.goal.id, 'step_id': step.id}),
            follow=False)

        self.assertRedirects(response,
                             reverse('new_step',
                                     kwargs={'goal_id': self.goal.id}))

        step.refresh_from_db()
        self.assertEquals('', step.comments)

        step_complete_signal.send.assert_called_with(
            'app.views.steps.track', step=step)

    @patch('app.views.steps.step_complete', spec=Signal)
    def test_track_last_five_day_step_redirects_to_feedback(
            self, step_complete_signal):

        for i in range(5):
            fixtures.step(self.goal)

        track_step_url = reverse('complete_step', kwargs={
            'goal_id': self.goal.id,
            'step_id': self.goal.current_step.id})

        response = self.client.post(track_step_url, follow=False)

        self.assertRedirects(response, reverse('feedback'))

    def test_new_to_track_redirect(self):
        step = fixtures.step(self.goal)

        new_step_url = reverse('new_step', kwargs={'goal_id': self.goal.id})
        response = self.client.get(new_step_url, follow=False)

        self.assertRedirects(response, reverse('complete_step', kwargs={
            'goal_id': self.goal.id, 'step_id': step.id}))

    def test_latest_404_on_no_goal(self):
        response = self.client.get(reverse('latest_step', kwargs={
            'goal_id': uuid4()}))

        self.assertEquals(404, response.status_code)

    def test_latest_redirects_to_new_step(self):
        response = self.client.get(reverse('latest_step', kwargs={
            'goal_id': self.goal.id}))

        self.assertRedirects(response, reverse('new_step', kwargs={
            'goal_id': self.goal.id}))

    def test_latest_redirects_to_last_step(self):
        step1 = fixtures.step(self.goal)

        response = self.client.get(reverse('latest_step', kwargs={
            'goal_id': self.goal.id}))

        self.assertRedirects(response, reverse('complete_step', kwargs={
            'goal_id': self.goal.id, 'step_id': step1.id}))

        step2 = fixtures.step(self.goal)

        response = self.client.get(reverse('latest_step', kwargs={
            'goal_id': self.goal.id}))

        self.assertRedirects(response, reverse('complete_step', kwargs={
            'goal_id': self.goal.id, 'step_id': step2.id}))
