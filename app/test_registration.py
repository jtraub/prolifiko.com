from django.test import TestCase, Client
from django.contrib.auth.models import User


class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_view(self):
        response = self.client.get('/app/register/')

        self.assertEqual(200, response.status_code)

    def test_register(self):
        response = self.client.post('/app/register/', {
            'username': 'new',
            'email': 'new@test.com',
            'password1': 'test',
            'password2': 'test',
        })

        self.assertRedirects(response, '/app/')

        user = User.objects.get(username='new')
        self.assertEqual('new@test.com', user.email)