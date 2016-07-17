from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from unittest.mock import patch, Mock


class AccountTest(TestCase):
    fixtures = ['users']

    token_generator = PasswordResetTokenGenerator()

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

    def test_password_reset_request(self):
        response = self.client.get(reverse('password_reset'))

        self.assertEquals(response.status_code, 200)

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_email(self):
        user = User.objects.create(
            email='password_reset@t.com', username='password_reset')
        user.set_password('test')
        user.save()
        client = Client()
        client.login(username='password_reset', password='test')

        response = client.post(reverse('password_reset'), {
            'email': user.email
        })

        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEquals(len(mail.outbox), 1)

        message = mail.outbox[0]
        self.assertTrue(isinstance(message, EmailMultiAlternatives))
        self.assertEquals(message.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertIsNotNone(message.body)
        self.assertIsNotNone(message.alternatives)
        # alternatives is a list of tuples of content and mimetype
        self.assertEquals(message.alternatives[0][1], 'text/html')

    def test_password_reset_done(self):
        response = self.client.get(reverse('password_reset_done'))

        self.assertEquals(response.status_code, 200)

    # TODO: Fix these tests!
    # def test_reset_password_confirm_form(self):
    #     uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
    #     token = self.token_generator.make_token(self.user)
    #     print(uidb64, token)
    #
    #     url = reverse('password_reset_confirm',
    #                   kwargs={'uidb64': uidb64, 'token': token})
    #     response = self.client.get(url)
    #
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTrue(response.context['validlink'])
    #
    # def test_reset_password_confirm(self):
    #     uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
    #     token = self.token_generator.make_token(self.user)
    #
    #     data = {'new_password1': '1234'}
    #     url = reverse('password_reset_confirm',
    #                   kwargs={'uidb64': uidb64, 'token': token})
    #     response = self.client.post(url, data=data, follow=False)
    #
    #     self.assertRedirects(response, reverse('password_reset_done'))

    def test_reset_password_complete(self):
        response = self.client.get(reverse('password_reset_complete'))

        self.assertEquals(response.status_code, 200)
