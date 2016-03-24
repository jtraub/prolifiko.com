from django.test import TestCase, Client

class AppTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/app', follow=True)

        self.assertContains(response, 'App Home', 1, 200)