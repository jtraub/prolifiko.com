from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from metrics import data


class DataTest(TestCase):
    @override_settings(
        TEST_EMAIL_ADDRESSES=['foo@bar.com', 'such@wow.com'],
        TEST_EMAIL_DOMAINS=['@test.com', '@t.com']
    )
    def test_real_users(self):
        emails = [
            'foo@bar.com',
            'such@wow.com',
            'test@test.com',
            'test@t.com',
            't@t.com'
        ]

        for email in emails:
            User.objects.create(email=email, username=email)

        User.objects.create(email='staff@real.com', username='staff',
                            is_staff=True)

        real_users = [user.email for user in data.real_users()]

        for email in emails:
            self.assertNotIn(email, real_users)

        self.assertNotIn('staff@real.com', real_users)
