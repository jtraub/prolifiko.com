from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.dispatch import Signal
from unittest.mock import patch

from app.views import auth as views


class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_view(self):
        response = self.client.get(reverse('app_register'))

        self.assertEqual(200, response.status_code)

    def test_no_email(self):
        response = self.client.post(reverse('app_register'), {
            'password': 'test',
        }, follow=True)

        self.assertEqual(400, response.status_code)
        self.assertEqual(0, len(response.redirect_chain))
        self.assertTrue(response.context['form'].has_error('email'))

    @override_settings(DEBUG=True)
    @patch('app.views.auth.registration', spec=Signal)
    def test_register(self, registration_signal):
        response = self.client.post(reverse('app_register'), {
            'email': 'new@test.com',
            'password': 'test',
            'first_name': 'name',
        }, follow=True)

        self.assertContains(response, 'check your inbox', status_code=201)

        user = User.objects.get(email='new@test.com')
        self.assertEqual('new@test.com', user.email)
        self.assertEqual('name', user.first_name)
        # We should have generated a username
        self.assertIsNotNone(user.username)
        # User.username.max_length=30
        self.assertTrue(len(user.username) <= 30)

        registration_signal.send.assert_called_with(
            'app.views.auth.register', user=user)

    def test_register_existing_email(self):
        User.objects.create(email='already@test.com')

        response = self.client.post(reverse('app_register'), {
            'email': 'already@test.com',
            'password': 'test',
            'first_name': 'name',
        }, follow=True)

        self.assertEquals(400, response.status_code)

        self.assertEquals(['Email address already registered'],
                          response.context['form'].errors['email'])
