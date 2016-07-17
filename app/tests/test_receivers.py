from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch

from app.models import Step, Goal
from app.receivers import *


@patch('app.receivers.send_email', spec=send_email)
@patch('app.receivers.add_event', spec=add_event)
class ReceiversTest(TestCase):
    fixtures = ['goals', 'steps']

    def setUp(self):
        self.user = User.objects.get(username='test')
        self.step = Step.objects.first()

    def test_registration_event(self, add_event, send_email):
        user = User.objects.first()

        receive_registration(self, user=user)

        add_event.assert_called_with('register', user)

    def test_registration_email(self, add_event, send_email):
        user = User.objects.first()

        receive_registration(self, user=user)

        send_email.assert_called_with('n1_registration', user)

    def test_new_goal_event(self, add_event, send_email):
        goal = Goal.objects.first()

        receive_new_goal(self, goal=goal)

        add_event.assert_called_with('goals.new', goal.user, {
            'goal_id': goal.id.hex
        })

    def test_goal_complete_event(self, add_event, send_email):
        goal = Goal.objects.first()

        receive_goal_complete(self, goal=goal)

        add_event.assert_called_with('goals.complete', goal.user, {
            'goal_id': goal.id.hex
        })

        send_email.assert_called_with('n7_goal_complete', goal.user, goal)

    def test_new_step_event(self, add_event, send_email):
        receive_new_step(self, step=self.step)

        add_event.assert_called_with('steps.new', self.step.goal.user, {
            'goal_id': self.step.goal.id.hex,
            'step_id': self.step.id.hex,
            'step_num': self.step.number
        })

    def test_new_step_email(self, add_event, send_email):
        goal = Goal.objects.create(user=self.user, text='test')

        step = Step.create(goal, 'test')

        receive_new_step(self, step=step)

        send_email.assert_called_with('n2_new_goal', goal.user, goal)
        add_event.assert_called_with('challenge.start', goal.user)

        for i in range(1, 4):
            step = Step.create(goal, 'test')

            receive_new_step(self, step=step)

            send_email.assert_called_with('n%d_step_%d_complete' % (i+2, i),
                                          goal.user, goal)

    def test_step_complete_event(self, add_event, send_email):
        receive_step_complete(self, step=self.step)

        add_event.assert_called_with('steps.track', self.step.goal.user, {
            'goal_id': self.step.goal.id.hex,
            'step_id': self.step.id.hex,
            'step_num': self.step.number
        })
