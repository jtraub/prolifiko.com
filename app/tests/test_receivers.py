from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch
from django.utils import timezone

from app.models import Step, Goal
from app.receivers import *
from app import fixtures


@patch('app.receivers.send_email', spec=send_email)
@patch('app.receivers.add_event', spec=add_event)
class ReceiversTest(TestCase):
    def setUp(self):
        self.user = fixtures.user('receivers@t.com', subscribed=False)
        self.five_day = fixtures.five_day_challenge(self.user)
        self.five_day_step = fixtures.step(self.five_day)
        self.goal = fixtures.goal(self.user)
        self.step = fixtures.step(self.goal)

    def test_registration(self, add_event, send_email):
        receive_registration(self, user=self.user)

        add_event.assert_called_with('register', self.user, {
            'timezone': 'Europe/London'
        })

        send_email.assert_called_with('n1_registration', self.user)

    def test_registration_subscribed(self, add_event, send_email):
        user = fixtures.user('subscribed@t.com')

        receive_registration(self, user=user)

        add_event.assert_called_with('subscribe', user)

    def test_new_five_day(self, add_event, send_email):
        receive_new_goal(self, goal=self.five_day)

        add_event.assert_called_with('goals.new', self.goal.user, {
            'goal_id': self.five_day.id.hex,
            'goal_type': Goal.TYPE_FIVE_DAY
        })

        send_email.assert_called_with('n2_new_goal', self.user, self.five_day)

    def test_new_goal(self, add_event, send_email):
        user = fixtures.user('new_goal_test@t.com')
        goal = fixtures.goal(user)
        receive_new_goal(self, goal=goal)

        add_event.assert_called_with('goals.new', user, {
            'goal_id': goal.id.hex,
            'goal_type': Goal.TYPE_CUSTOM
        })

        send_email.assert_called_with('new_custom_goal', user, goal)

    def test_new_goal_only_sends_email_for_first_goal(self,
                                                      add_event,
                                                      send_email):
        second_goal = fixtures.goal(self.user)

        receive_new_goal(self, goal=second_goal)

        add_event.assert_called_with('goals.new', self.user, {
            'goal_id': second_goal.id.hex,
            'goal_type': Goal.TYPE_CUSTOM
        })

        send_email.assert_not_called()

    def test_five_day_complete(self, add_event, send_email):
        receive_goal_complete(self, goal=self.five_day)

        add_event.assert_called_with('goals.complete', self.user, {
            'goal_id': self.five_day.id.hex,
            'goal_type': Goal.TYPE_FIVE_DAY
        })

        send_email.assert_called_with('n7_goal_complete',
                                      self.user,
                                      self.five_day)

    def test_goal_complete(self, add_event, send_email):
        receive_goal_complete(self, goal=self.goal)

        add_event.assert_called_with('goals.complete', self.goal.user, {
            'goal_id': self.goal.id.hex,
            'goal_type': Goal.TYPE_CUSTOM
        })

    def test_new_five_day_step(self, add_event, send_email):
        goal = fixtures.five_day_challenge(self.user)
        step = fixtures.step(goal)

        for i in range(1, 4):
            step = fixtures.step(goal)

            receive_new_step(self, step=step)

            send_email.assert_called_with('n%d_step_%d_complete' % (i+2, i),
                                          goal.user, goal)

    def test_new_step(self, add_event, send_email):
        receive_new_step(self, step=self.step)

        add_event.assert_called_with('steps.new', self.step.goal.user, {
            'goal_id': self.goal.id.hex,
            'goal_type': Goal.TYPE_CUSTOM,
            'step_id': self.step.id.hex,
            'step_num': self.step.number
        })

        send_email.assert_not_called()

    def test_five_day_step_complete(self, add_event, send_email):
        receive_step_complete(self, step=self.five_day_step)

        add_event.assert_called_with('steps.complete', self.user, {
            'goal_id': self.five_day.id.hex,
            'goal_type': Goal.TYPE_FIVE_DAY,
            'step_id': self.five_day_step.id.hex,
            'step_num': self.five_day_step.number
        })

        send_email.assert_not_called()

    def test_step_complete(self, add_event, send_email):
        receive_step_complete(self, step=self.step)

        add_event.assert_called_with('steps.complete', self.user, {
            'goal_id': self.goal.id.hex,
            'goal_type': Goal.TYPE_CUSTOM,
            'step_id': self.step.id.hex,
            'step_num': self.step.number
        })

        send_email.assert_not_called()
