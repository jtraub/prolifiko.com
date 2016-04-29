from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from unittest.mock import patch


class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_view(self):
        response = self.client.get(reverse('app_register'))

        self.assertEqual(200, response.status_code)

    def test_no_email(self):
        response = self.client.post(reverse('app_register'), {
            'first_name': 'new',
            'password1': 'test',
            'password2': 'test',
        }, follow=True)

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.redirect_chain))
        self.assertTrue(response.context['form'].has_error('email'))

    def test_no_first_name(self):
        response = self.client.post(reverse('app_register'), {
            'email': 'new@test.com',
            'password1': 'test',
            'password2': 'test',
        }, follow=True)

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.redirect_chain))
        self.assertTrue(response.context['form'].has_error('first_name'))

    @patch('app.views.auth.keen')
    def test_register(self, keen):
        response = self.client.post(reverse('app_register'), {
            'email': 'new@test.com',
            'first_name': 'new',
            'password1': 'test',
            'password2': 'test',
        }, follow=True)

        redirect_to_index = (reverse('app_index'), 302)
        self.assertEquals(redirect_to_index, response.redirect_chain[0])

        user = User.objects.get(email='new@test.com')
        self.assertEqual('new@test.com', user.email)
        self.assertEqual('new', user.first_name)
        # We should have generated a username
        self.assertIsNotNone(user.username)
        # User.username.max_length=30
        self.assertTrue(len(user.username) <= 30)

        keen.add_event.assert_called_with('register', {
            'id': user.id,
            'email': user.email
        })
