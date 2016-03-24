from django.test import TestCase, Client


class AuthTest(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.client = Client()

    def test_auth_redirect(self):
        response = self.client.get('/app/')

        self.assertRedirects(response, '/app/login/?next=/app/')

    def test_login_view(self):
        response = self.client.get('/app/login/')

        self.assertEqual(200, response.status_code)

    def test_login(self):
        response = self.client.post('/app/login/', {'username': 'test', 'password': 'test'})

        self.assertRedirects(response, '/app/')

    def test_login_error(self):
        response = self.client.post('/app/login/', {'username': 'nope', 'password': 'nope'})

        self.assertEqual(200, response.status_code)
