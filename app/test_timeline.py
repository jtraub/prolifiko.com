from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Goal, Step


class TimelineTest(TestCase):
    fixtures = ['users', 'goals']

    def setUp(self):
        self.client = Client()
        self.client.login(username='empty', password='test')

        self.user = User.objects.get(username="test")
        self.goal = Goal.objects.filter(user=self.user).first()

    def test_shows_new_step_link_if_none_in_progress(self):
        self.client.login(username='empty', password='test')

        Step.objects.create(goal=self.goal, complete=True,
                            start=timezone.now(), end=timezone.now())

        response = self.client.get(reverse('app_goals_timeline',
                                           kwargs={'goal_id': self.goal.id}))

        self.assertContains(response, 'Create your next step')
