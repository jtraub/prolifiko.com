from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class AppTest(TestCase):
    fixtures = ['users', 'goals']

    def setUp(self):
        self.client = Client()

    # def test_index(self):
    #     self.client.login(username='test', password='test')
    #     response = self.client.get(reverse('app_index'))
    #
    #     self.assertContains(response, 'App')

    def test_redirects_to_new_goal_if_none(self):
        self.client.login(username='empty', password='test')
        response = self.client.get(reverse('app_index'))

        self.assertRedirects(response, reverse('app_goals_new'))
