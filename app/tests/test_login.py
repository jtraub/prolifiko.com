from unittest import skip
from django.core.exceptions import NON_FIELD_ERRORS
from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from unittest.mock import patch

from app.utils import add_event


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_auth_redirect(self):
        response = Client().get(reverse('index'))

        login_url = reverse('login') + '?next=' + reverse('index')
        self.assertRedirects(response, login_url)

    def test_login_view(self):
        response = Client().get(reverse('login'))

        self.assertEqual(200, response.status_code)

    @override_settings(DEBUG=True)
    @patch('app.views.auth.add_event', spec=add_event)
    def test_login(self, add_event):
        response = Client().post(reverse('login'), {
            'email': 'test@test.com',
            'password': 'test'
        }, follow=True)

        redirect_to_index = (reverse('index'), 302)
        self.assertEquals(redirect_to_index, response.redirect_chain[0])

        user = User.objects.get(email='test@test.com')

        add_event.assert_called_with('login', user)

    def test_invalid(self):
        response = Client().post(reverse('login'), {
            'email': 'test@test.com',
        }, follow=True)

        self.assertEqual(200, response.status_code)
        self.assertEquals(0, len(response.redirect_chain))
        self.assertTrue(response.context['form'].has_error('password'))

    def test_bad_email(self):
        response = Client().post(reverse('login'), {
            'email': 'nope@test.com',
            'password': 'nope',
        }, follow=True)

        self.assertEqual(200, response.status_code)
        self.assertEquals(0, len(response.redirect_chain))
        self.assertTrue(response.context['form'].has_error(
                        NON_FIELD_ERRORS, 'bad_email'))

    def test_bad_password(self):
        response = Client().post(reverse('login'), {
            'email': 'test@test.com',
            'password': 'nope'
        }, follow=True)

        self.assertEqual(200, response.status_code)
        self.assertEquals(0, len(response.redirect_chain))
        self.assertTrue(response.context['form'].has_error(
                        NON_FIELD_ERRORS, 'bad_password'))

    @skip
    def test_deactivated(self):
        user = User.objects.create(email='inactive@t.com')
        user.set_password('test1234')
        user.is_active = False
        user.save()

        response = Client().post(reverse('login'), {
            'email': user.email,
            'password': 'test'
        }, follow=False)

        print(response.context['form'])

        self.assertRedirects(response, reverse('deactivate',
                                               kwargs={'user_id': user.id}))
