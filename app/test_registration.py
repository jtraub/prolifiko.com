from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.dispatch import Signal
from unittest.mock import patch

from .views import auth as views


class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_view(self):
        response = self.client.get(reverse('app_register'))

        self.assertEqual(200, response.status_code)

    def test_no_email(self):
        response = self.client.post(reverse('app_register'), {
            'password1': 'test',
            'password2': 'test',
        }, follow=True)

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.redirect_chain))
        self.assertTrue(response.context['form'].has_error('email'))

    @override_settings(DEBUG=True)
    @patch('app.views.auth.registration', spec=Signal)
    def test_register(self, registration_signal):
        response = self.client.post(reverse('app_register'), {
            'email': 'new@test.com',
            'password1': 'test',
            'password2': 'test',
        }, follow=True)

        self.assertEquals(201, response.status_code)
        self.assertContains(response, 'Check your inbox')

        user = User.objects.get(email='new@test.com')
        self.assertEqual('new@test.com', user.email)
        self.assertEqual('new', user.first_name)
        # We should have generated a username
        self.assertIsNotNone(user.username)
        # User.username.max_length=30
        self.assertTrue(len(user.username) <= 30)

        registration_signal.send.assert_called_with(views.register, user=user)
