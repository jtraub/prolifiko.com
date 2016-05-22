from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from unittest.mock import patch, Mock

from app.tasks import *
from app.models import Step, Goal


@patch('django.core.mail.utils.socket')
class TasksTest(TestCase):
    def test_send_dr_emails(self, socket):
        socket.getfqdn = Mock(return_value='test')

        now = timezone.now()

        recent_user = User.objects.create(
            username='recent',
            email='recent@t.com',
        )

        active_user = User.objects.create(
            username='active',
            email='active@t.com',
        )
        Goal.objects.create(user=active_user, text='test')

        dr1_user = User.objects.create(
            username='dr1',
            date_joined=now - timedelta(hours=24),
            email='dr1@t.com'
        )

        dr2_user = User.objects.create(
            username='dr2',
            date_joined=now - timedelta(hours=48),
            email='dr2@t.com'
        )

        dr3_user = User.objects.create(
            username='dr3',
            date_joined=now - timedelta(hours=72),
            email='dr3@t.com'
        )

        send_dr_emails()

        self.assertEquals(3, len(mail.outbox))

        emails = [{'subject': email.subject, 'to': email.to[0]}
                  for email in mail.outbox]

        self.assertIn({
            'subject': settings.EMAIL_META['dr1']['subject'],
            'to': dr1_user.email
        }, emails)

        self.assertIn({
            'subject': settings.EMAIL_META['dr2']['subject'],
            'to': dr2_user.email
        }, emails)

        self.assertIn({
            'subject': settings.EMAIL_META['dr3']['subject'],
            'to': dr3_user.email
        }, emails)
