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

        emails = [{'name': email.prolifiko_name, 'to': email.to[0]}
                  for email in mail.outbox]

        self.assertIn({
            'name': 'dr1',
            'to': dr1_user.email
        }, emails)

        self.assertIn({
            'name': 'dr2',
            'to': dr2_user.email
        }, emails)

        self.assertIn({
            'name': 'dr3',
            'to': dr3_user.email
        }, emails)

    def test_send_d_emails(self, socket):
        socket.getfqdn = Mock(return_value='test')

        now = timezone.now()

        active_user1 = User.objects.create(
            username='active1',
            email='active@t.com',
        )
        Step.objects.create(
            goal=Goal.objects.create(user=active_user1, text='test'),
            start=now - timedelta(hours=2),
            end=now + timedelta(hours=22)
        )

        active_user2 = User.objects.create(
            username='active2',
            email='active@t.com',
        )
        Step.objects.create(
            goal=Goal.objects.create(user=active_user2, text='test'),
            start=now - timedelta(hours=64),
            end=now - timedelta(hours=40),
            complete=True
        )

        d1_user = User.objects.create(
            username='d1',
            email='d1@t.com',
        )
        d1_goal = Goal.objects.create(user=d1_user, text='test')
        Step.objects.create(
            goal=d1_goal,
            text='test',
            start=now - timedelta(hours=48),
            end=now - timedelta(hours=24)
        )

        d2_user = User.objects.create(
            username='d2',
            email='d2@t.com',
        )
        d2_goal = Goal.objects.create(user=d2_user, text='test', lives=2)
        Step.objects.create(
            goal=d2_goal,
            text='test',
            start=now - timedelta(hours=72),
            end=now - timedelta(hours=48)
        )

        d3_user = User.objects.create(
            username='d3',
            email='d3@t.com',
        )
        d3_goal = Goal.objects.create(user=d3_user, text='test', lives=1)
        Step.objects.create(
            goal=d3_goal,
            text='test',
            start=now - timedelta(hours=96),
            end=now - timedelta(hours=72)
        )

        send_d_emails()

        self.assertEquals(3, len(mail.outbox))

        emails = [{'name': email.prolifiko_name, 'to': email.to[0]}
                  for email in mail.outbox]

        d1_goal.refresh_from_db()
        self.assertEquals(2, d1_goal.lives)
        self.assertIn({
            'name': 'd1',
            'to': d1_user.email
        }, emails)

        d2_goal.refresh_from_db()
        self.assertEquals(1, d2_goal.lives)
        self.assertIn({
            'name': 'd2',
            'to': d2_user.email
        }, emails)

        d3_goal.refresh_from_db()
        self.assertEquals(0, d3_goal.lives)
        self.assertIn({
            'name': 'd3',
            'to': d3_user.email
        }, emails)
