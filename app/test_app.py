from django.test import TestCase, Client


class AppTest(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_index(self):
        response = self.client.get('/app/')

        self.assertEqual(200, response.status_code)

    def test_shows_username(self):
        response = self.client.get('/app/')

        self.assertContains(response, 'test')
