from django.core.exceptions import NON_FIELD_ERRORS
from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from app.utils import events


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_auth_redirect(self):
        response = Client().get(reverse('app_index'))

        self.assertRedirects(response, '/app/login/?next=/app/')

    def test_login_view(self):
        response = Client().get(reverse('app_login'))

        self.assertEqual(200, response.status_code)

    @override_settings(DEBUG=True)
    def test_login(self):
        response = Client().post(reverse('app_login'), {
            'email': 'test@test.com',
            'password': 'test'
        }, follow=True)

        redirect_to_index = (reverse('app_index'), 302)
        self.assertEquals(redirect_to_index, response.redirect_chain[0])

        user = User.objects.get(email='test@test.com')

        self.assertEquals(events.pop(), {
            'collection': 'login',
            'body': {
                'id': user.id,
                'email': user.email
            }
        })

    def test_invalid(self):
        response = Client().post(reverse('app_login'), {
            'email': 'test@test.com',
        }, follow=True)

        self.assertEqual(200, response.status_code)
        self.assertEquals(0, len(response.redirect_chain))
        self.assertTrue(response.context['form'].has_error('password'))

    def test_bad_email(self):
        response = Client().post(reverse('app_login'), {
            'email': 'nope@test.com',
            'password': 'nope',
        }, follow=True)

        self.assertEqual(200, response.status_code)
        self.assertEquals(0, len(response.redirect_chain))
        self.assertTrue(response.context['form'].has_error(
                        NON_FIELD_ERRORS, 'bad_email'))

    def test_bad_password(self):
        response = Client().post(reverse('app_login'), {
            'email': 'test@test.com',
            'password': 'nope'
        }, follow=True)

        self.assertEqual(200, response.status_code)
        self.assertEquals(0, len(response.redirect_chain))
        self.assertTrue(response.context['form'].has_error(
                        NON_FIELD_ERRORS, 'bad_password'))

    def test_deactivated(self):
        user = User.objects.create(email='inactive@t.com')
        user.set_password('test')
        user.is_active = False
        user.save()

        response = Client().post(reverse('app_login'), {
            'email': user.email,
            'password': 'test'
        }, follow=False)

        self.assertRedirects(response, reverse('app_deactivate',
                                               kwargs={'user_id': user.id}))
