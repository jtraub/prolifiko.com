from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class FiveDayChallengeTest(TestCase):
    def test_redirects_to_new_goal_if_empty(self):
        client = Client()
        client.login(username='empty', password='test')
        response = client.get(reverse('myprogress'), follow=False)

        self.assertRedirects(response, reverse('new_goal'))
