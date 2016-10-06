from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from app.models import Goal


class AppTest(TestCase):
    fixtures = ['users', 'goals']

    def test_redirects_to_new_goal_if_empty(self):
        client = Client()
        client.login(username='empty', password='test')
        response = client.get(reverse('index'), follow=False)

        self.assertRedirects(response, reverse('new_goal'))

    def test_redirects_to_my_progress(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('index'), follow=True)

        goal = Goal.objects.filter(user__username='test').first()

        myprogress_url = reverse('app_goals_timeline',
                                 kwargs={'goal_id': goal.id})

        self.assertEquals(response.redirect_chain[0],
                          (myprogress_url, 302))
