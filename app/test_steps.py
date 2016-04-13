from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from datetime import timedelta

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

    def test_new(self):
        text = uuid4()
        response = self.client.post(
            reverse('app_steps_new', kwargs={'goal_id': self.goal.id}),
            data={'text': text},
            follow=False
        )

        step = Step.objects.get(text=text)

        self.assertRedirects(response, reverse('app_steps_congrats',
                                               kwargs={'goal_id': self.goal.id,
                                                       'step_id': step.id}))

        self.assertIsNotNone(step)
        self.assertEquals(self.goal.id, step.goal.id)
        self.assertAlmostEquals(timezone.now(), step.start,
                                delta=timedelta(seconds=3))
        self.assertEquals(step.start + timedelta(days=1), step.end)
