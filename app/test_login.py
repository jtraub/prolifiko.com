from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class LoginTest(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.client = Client()

    def test_auth_redirect(self):
        response = self.client.get(reverse('app_index'))

        self.assertRedirects(response, '/app/login/?next=/app/')

    def test_login_view(self):
        response = self.client.get(reverse('app_login'))

        self.assertEqual(200, response.status_code)

    def test_login(self):
        response = self.client.post(reverse('app_login'), {
            'username': 'test',
            'password': 'test'
        }, follow=True)

        redirect_to_index = (reverse('app_index'), 302)
        self.assertEquals(redirect_to_index, response.redirect_chain[0])

    def test_login_error(self):
        response = self.client.post(reverse('app_login'), {
            'username': 'nope',
            'password': 'nope'
        })

        self.assertEqual(200, response.status_code)
