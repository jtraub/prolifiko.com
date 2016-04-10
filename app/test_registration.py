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

    @patch('app.views.keen')
    def test_register(self, keen):
        response = self.client.post(reverse('app_register'), {
            'username': 'new',
            'email': 'new@test.com',
            'password1': 'test',
            'password2': 'test',
        }, follow=True)

        redirect_to_index = (reverse('app_index'), 302)
        self.assertEquals(redirect_to_index, response.redirect_chain[0])

        user = User.objects.get(username='new')
        self.assertEqual('new@test.com', user.email)

        keen.add_event.assert_called_with('register', {
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
