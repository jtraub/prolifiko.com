from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from app import fixtures

from app.models import Goal


class AppTest(TestCase):
    def test_redirects_to_new_goal_if_empty(self):
        client = fixtures.client()
        response = client.get(reverse('myprogress'), follow=False)

        self.assertRedirects(response, reverse('new_goal'))
