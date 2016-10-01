from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid1

from django.utils.timezone import now, pytz
from datetime import timedelta, datetime, time, date
from unittest.mock import patch
from django.dispatch import Signal

from app.models import Goal, Step, Timezone
from app.views import goals as views
from app import fixtures


class GoalsTest(fixtures.TestCase):
    def test_new_form(self):
        response = self.client.get(reverse('new_goal'))

        self.assertEquals(200, response.status_code, response)

    def test_new_form_redirects_to_existing_five_day_challenge(self):
        goal = fixtures.five_day_challenge(self.user)

        response = self.client.get(reverse('new_goal'), follow=True)

        goal_progress_url = reverse('goal_progress',
                                    kwargs={'id': goal.id})
        self.assertEquals(response.redirect_chain[0], (goal_progress_url, 302))

    @patch('app.views.goals.new_goal', spec=Signal)
    @patch('app.views.goals.new_step', spec=Signal)
    def test_new_five_day_challenge(self, new_step, new_goal):
        response = self.client.post(reverse('new_goal'), data={
            'type': 'FIVE_DAY_CHALLENGE',
            'goal_name': 'goal name',
            'goal_description': 'goal description',
            'first_step_name': 'step name',
            'first_step_description': 'step description',
        }, follow=False)

        goal = Goal.objects.filter(user=self.user).first()

        self.assertIsNotNone(goal, Goal.objects.filter(user=self.user))

        first_step = goal.steps.first()

        self.assertIsNotNone(first_step)

        self.assertRedirects(response, reverse('start_step', kwargs={
            'goal_id': goal.id, 'step_id': first_step.id}))

        self.assertIsNotNone(goal)
        self.assertEquals(3, goal.lives)
        self.assertAlmostEquals(timezone.now(), goal.start,
                                delta=timedelta(seconds=1))
        self.assertEquals((goal.start + timedelta(days=5)).date(), goal.target)
        self.assertEquals('goal name', goal.name)
        self.assertEquals('goal description', goal.description)

        self.assertEquals(1, len(goal.steps.all()))
        first_step = goal.steps.first()
        self.assertEquals('step name', first_step.name)
        self.assertEquals('step description', first_step.description)
        self.assertEquals(goal.start, first_step.start)
        tz = pytz.timezone('Europe/London')
        self.assertEquals(Step.midnight_deadline(first_step.start, tz),
                          first_step.deadline)

        new_goal.send.assert_called_with('app.views.goals.new',
                                         goal=goal)
        new_step.send.assert_called_with('app.views.goals.new',
                                         step=first_step)

    @patch('app.views.goals.new_goal', spec=Signal)
    @patch('app.views.goals.new_step', spec=Signal)
    def test_new_custom_goal(self, new_step, new_goal):
        response = self.client.post(reverse('new_goal'), data={
            'type': 'CUSTOM',
            'goal_name': 'goal name',
            'goal_description': 'goal description',
            'goal_target': '2016-01-07',
            'first_step_name': 'step name',
            'first_step_description': 'step description',
            'first_step_deadline': '2016-01-02',
        }, follow=False)

        goal = Goal.objects.filter(user=self.user).first()

        self.assertIsNotNone(goal, Goal.objects.filter(user=self.user))

        first_step = goal.steps.first()

        self.assertIsNotNone(first_step)

        self.assertRedirects(response, reverse('start_step', kwargs={
            'goal_id': goal.id, 'step_id': first_step.id}))

        self.assertIsNotNone(goal)
        self.assertAlmostEquals(timezone.now(), goal.start,
                                delta=timedelta(seconds=1))
        self.assertEquals(date(2016, 1, 7), goal.target)
        self.assertEquals('goal name', goal.name)
        self.assertEquals('goal description', goal.description)

        self.assertEquals(1, len(goal.steps.all()))
        first_step = goal.steps.first()
        self.assertEquals('step name', first_step.name)
        self.assertEquals('step description', first_step.description)
        self.assertEquals(goal.start, first_step.start)
        expected_deadline = pytz.timezone('Europe/London') \
            .localize(datetime(2016, 1, 2, 0)) \
            .astimezone(pytz.utc)
        self.assertEquals(expected_deadline, first_step.deadline)

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
