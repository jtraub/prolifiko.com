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
        self.user = User.objects.get(username='test')
        self.goal = fixtures.goal(self.user)
        self.step = fixtures.step(self.goal)

    def test_registration_event(self, add_event, send_email):
        user = User.objects.first()

        receive_registration(self, user=user)

        add_event.assert_called_with('register', user)

    def test_registration_email(self, add_event, send_email):
        user = User.objects.first()

        receive_registration(self, user=user)

        send_email.assert_called_with('n1_registration', user)

    def test_new_goal_event(self, add_event, send_email):
        receive_new_goal(self, goal=self.goal)

        add_event.assert_called_with('goals.new', self.goal.user, {
            'goal_id': self.goal.id.hex
        })

    def test_goal_complete_event(self, add_event, send_email):
        receive_goal_complete(self, goal=self.goal)

        add_event.assert_called_with('goals.complete', self.goal.user, {
            'goal_id': self.goal.id.hex
        })

        send_email.assert_called_with('n7_goal_complete',
                                      self.goal.user,
                                      self.goal)

    def test_new_step_event(self, add_event, send_email):
        receive_new_step(self, step=self.step)

        add_event.assert_called_with('steps.new', self.step.goal.user, {
            'goal_id': self.step.goal.id.hex,
            'step_id': self.step.id.hex,
            'step_num': self.step.number
        })

    def test_new_step_email(self, add_event, send_email):
        goal = fixtures.goal(self.user)
        step = fixtures.step(goal)

        receive_new_step(self, step=step)

        send_email.assert_called_with('n2_new_goal', goal.user, goal)

        for i in range(1, 4):
            step = step = fixtures.step(goal)

            receive_new_step(self, step=step)

            send_email.assert_called_with('n%d_step_%d_complete' % (i+2, i),
                                          goal.user, goal)

    def test_step_complete_event(self, add_event, send_email):
        receive_step_complete(self, step=self.step)

        add_event.assert_called_with('steps.complete', self.step.goal.user, {
            'goal_id': self.step.goal.id.hex,
            'step_id': self.step.id.hex,
            'step_num': self.step.number
        })
