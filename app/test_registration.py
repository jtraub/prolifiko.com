from django.test import TestCase, Client
from django.contrib.auth.models import User
from unittest.mock import patch


class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_view(self):
        response = self.client.get('/app/register/')

        self.assertEqual(200, response.status_code)

    @patch('app.views.keen')
    def test_register(self, keen):
        response = self.client.post('/app/register/', {
            'username': 'new',
            'email': 'new@test.com',
            'password1': 'test',
            'password2': 'test',
        })

        self.assertRedirects(response, '/app/')

        user = User.objects.get(username='new')
        self.assertEqual('new@test.com', user.email)

        keen.add_event.assert_called_with('register', {
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
