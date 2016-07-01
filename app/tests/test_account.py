from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from unittest.mock import patch


@patch('app.views.account.add_event')
class AccountTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_deactivate_400_on_bad_user(self, add_event):
        response = self.client.get(reverse('app_deactivate',
                                           kwargs={'user_id': '0'}))

        self.assertEquals(response.status_code, 400)

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

    def test_user_is_not_deactivated_if_already_inactive(self, add_event):
        user = User.objects.create(email='already_inactive@t.com')
        user.is_active = False
        user.save()

        response = self.client.get(reverse('app_deactivate',
                                           kwargs={'user_id': user.id}))

        self.assertContains(response, 'Your account has been deactivated')

        self.assertFalse(add_event.called)
