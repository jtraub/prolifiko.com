from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from unittest.mock import patch, Mock


class AccountTest(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='test')
        self.client.login(username='test', password='test')

    def test_deactivate_400_on_bad_user(self):
        response = self.client.get(reverse('app_deactivate',
                                           kwargs={'user_id': '0'}))

        self.assertEquals(response.status_code, 400)

    @patch('app.views.account.add_event')
    def test_user_is_deactivated(self, add_event):
        user = User.objects.create(email='deactivate@t.com')

        response = self.client.get(reverse('app_deactivate',
                                           kwargs={'user_id': user.id}))

        self.assertContains(response, 'Your account has been deactivated')

        user.refresh_from_db()
        self.assertFalse(user.is_active)

        add_event.assert_called_with('deactivate', {
            'id': user.id,
            'email': user.email
        })

    @patch('app.views.account.add_event')
    def test_user_is_not_deactivated_if_already_inactive(self, add_event):
        user = User.objects.create(email='already_inactive@t.com')
        user.is_active = False
        user.save()

        response = self.client.get(reverse('app_deactivate',
                                           kwargs={'user_id': user.id}))

        self.assertContains(response, 'Your account has been deactivated')

        self.assertFalse(add_event.called)

    def test_reset_password(self):
        response = self.client.get(reverse('password_reset'))

        self.assertEquals(response.status_code, 200)

    def test_reset_passwort_done(self):
        response = self.client.get(reverse('password_reset_done'))

        self.assertEquals(response.status_code, 200)

    @patch('django.contrib.auth.views.default_token_generator')
    def test_reset_password_confirm(self, token_generator):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))
        token_generator.check_token = Mock(return_value=True)

        response = self.client.get(reverse('password_reset_confirm',
                                           kwargs={
                                               'uidb64': uidb64,
                                               'token': '12-34'
                                           }))

        self.assertEquals(response.status_code, 200)

    def test_reset_password_complete(self):
        response = self.client.get(reverse('password_reset_complete'))

        self.assertEquals(response.status_code, 200)
