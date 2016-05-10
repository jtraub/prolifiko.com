from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch

from .models import Step, Goal
from .receivers import *


@patch('app.receivers.send_email', spec=send_email)
@patch('app.receivers.add_event', spec=add_event)
class ReceiversTest(TestCase):
    fixtures = ['users', 'goals', 'steps']

    def setUp(self):
        self.user = User.objects.get(username='test')
        self.step = Step.objects.first()

    def test_new_goal_event(self, add_event, send_email):
        goal = Goal.objects.first()

        receive_new_goal(None, goal=goal)

        add_event.assert_called_with('goals.new', {
            'id': goal.id.hex,
            'user_id': goal.user.id,
        })

    def test_step_complete_event(self, add_event, send_email):
        receive_step_complete(None, step=self.step)

        add_event.assert_called_with('steps.track', {
            'id': self.step.id.hex,
            'user_id': self.step.goal.user.id,
            'goal_id': self.step.goal.id.hex
        })

    def test_step_complete_emails(self, add_event, send_email):
        goal = Goal.objects.create(user=self.user, text='test')

        for i in range(1, 5):
            step = Step.create(goal, 'test')

            receive_step_complete(None, step=step)

            send_email.assert_called_with('step_%d_complete' % i, goal.user, {
                'goal': goal
            })

    def test_new_step_event(self, add_event, send_email):
        receive_new_step(None, step=self.step)

        add_event.assert_called_with('steps.new', {
            'id': self.step.id.hex,
            'user_id': self.step.goal.user.id,
            'goal_id': self.step.goal.id.hex
        })

    def test_new_step_email(self, add_event, send_email):
        goal = Goal.objects.create(user=self.user, text='test')

        first_step = Step.create(goal, 'text')
        receive_new_step(None, step=first_step)
        send_email.assert_called_with('new_goal', goal.user, {'goal': goal})

        send_email.reset_mock()

        second_step = Step.create(goal, 'text')
        receive_new_step(None, step=second_step)
        send_email.assert_not_called()
