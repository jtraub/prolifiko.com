from django.test import TestCase, Client

class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get('/')

        self.assertContains(response, '<h1>Homepage</h1>', 1, 200)
