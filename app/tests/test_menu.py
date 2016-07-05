from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class MenuTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about(self):
        response = self.client.get(reverse('app_menu_about'))
        self.assertContains(response, 'About')

    def test_terms(self):
        response = self.client.get(reverse('app_menu_terms'))
        self.assertContains(response, 'Terms & Conditions')

    def test_privacy(self):
        response = self.client.get(reverse('app_menu_privacy'))
        self.assertContains(response, 'Privacy')

    def test_help(self):
        response = self.client.get(reverse('app_menu_help'))
        self.assertContains(response, 'Help')
