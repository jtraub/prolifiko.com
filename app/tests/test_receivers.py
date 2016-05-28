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

        add_event.assert_called_with('register', {
            'id': user.id,
            'email': user.email
        })

    def test_registration_email(self, add_event, send_email):
        user = User.objects.first()

        receive_registration(self, user=user)

        send_email.assert_called_with('n1_registration', user)

    def test_new_goal_event(self, add_event, send_email):
        goal = Goal.objects.first()

        receive_new_goal(self, goal=goal)

        add_event.assert_called_with('goals.new', {
            'id': goal.id.hex,
            'user_id': goal.user.id,
        })

    def test_new_step_event(self, add_event, send_email):
        receive_new_step(self, step=self.step)

        add_event.assert_called_with('steps.new', {
            'id': self.step.id.hex,
            'user_id': self.step.goal.user.id,
            'goal_id': self.step.goal.id.hex
        })

    def test_new_step_email(self, add_event, send_email):
        goal = Goal.objects.create(user=self.user, text='test')

        step = Step.create(goal, 'test')

        receive_new_step(self, step=step)

        send_email.assert_called_with('n2_new_goal', goal.user,
                                      {'first_step': step})

        for i in range(1, 4):
            step = Step.create(goal, 'test')

            receive_new_step(self, step=step)

            send_email.assert_called_with('n%d_step_%d_complete' % (i+2, i),
                                          goal.user, {'next_step': step})

    def test_step_complete_event(self, add_event, send_email):
        receive_step_complete(self, step=self.step)

        add_event.assert_called_with('steps.track', {
            'id': self.step.id.hex,
            'user_id': self.step.goal.user.id,
            'goal_id': self.step.goal.id.hex
        })
