from unittest import skip
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from app.models import Goal, Step


@skip
class IsActiveTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='isactive@t.com',
            username='isactive'
        )
        self.user.set_password('test')
        self.user.save()

        self.goal = Goal.objects.create(user=self.user, text='test',
                                        timezone='Europe/London',
                                        start=timezone.now())
        self.step = Step.create(self.goal, 'text')

        self.client = Client()
        self.client.login(username='isactive', password='test')

        self.user.is_active = False
        self.user.save()

    def test_views(self):
        urls = [
            reverse('new_goal'),
            reverse('app_goals_timeline', kwargs={'goal_id': self.goal.id}),
            reverse('complete_goal', kwargs={'goal_id': self.goal.id}),
            reverse('new_step', kwargs={'goal_id': self.goal.id}),
            reverse('start_step',
                    kwargs={'goal_id': self.goal.id, 'step_id': self.step.id}),
            reverse('complete_step',
                    kwargs={'goal_id': self.goal.id, 'step_id': self.step.id}),
        ]

        deactivate_url = reverse('deactivate',
                                 kwargs={'user_id': self.user.id})

        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, deactivate_url, msg_prefix=url)
