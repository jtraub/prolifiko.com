from unittest.mock import patch
from django.contrib.auth.models import User
from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from django.conf import settings


@override_settings(MAINTENANCE_MODE=True)
class MaintenanceTest(TestCase):
    def test_no_auth_redirected_to_login(self):
        response = Client().get(reverse('myprogress'), follow=False)
        self.assertRedirects(response, reverse('login'))

    def test_login_page_accessible(self):
        response = Client().get(reverse('login'))
        self.assertEquals(200, response.status_code)

    def test_registration_accessible(self):
        response = Client().get(reverse('register'), follow=False)
        self.assertEquals(200, response.status_code)

    def test_logged_in_users_shown_banner(self):
        user = User(username='real')
        user.email = 'real@real.com'
        user.set_password('test')
        user.save()

        client = Client()
        client.login(username='real', password='test')

        response = client.get(reverse('myprogress'), follow=False)

        self.assertRedirects(response, reverse('maintenance'))

    @patch('app.views.auth.add_event')
    def test_users_redirected_after_login(self, add_event):
        user = User(username='real')
        user.email = 'real@real.com'
        user.set_password('test')
        user.save()

        response = Client().post(reverse('login'), {
            'email': user.email,
            'password': 'test',
        }, follow=True)

        self.assertEquals(response.redirect_chain[-1],
                          (reverse('maintenance'), 302))

    def test_staff_not_redirected(self):
        user = User(username='staff')
        user.email = 'staff@real.com'
        user.is_staff = True
        user.set_password('test')
        user.save()

        client = Client()
        client.login(username='staff', password='test')

        response = client.get(reverse('new_goal'), follow=False)

        self.assertEquals(response.status_code, 200)

    def test_test_email_not_redirected(self):
        user = User(username='tester')
        user.email = settings.TEST_EMAIL_ADDRESSES[-1]
        user.set_password('test')
        user.save()

        client = Client()
        client.login(username='tester', password='test')

        response = client.get(reverse('new_goal'), follow=False)

        self.assertEquals(response.status_code, 200)

    def test_test_domain_not_redirected(self):
        user = User(username='tester')
        user.email = 'real@' + settings.TEST_EMAIL_DOMAINS[0]
        user.set_password('test')
        user.save()

        client = Client()
        client.login(username='tester', password='test')

        response = client.get(reverse('new_goal'), follow=False)

        self.assertEquals(response.status_code, 200)
