from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
import pytz
from app.models import Goal
from app.tasks import send_d_emails_at_midnight


@patch('django.core.mail.utils.socket')
class DEmailTest(TestCase):
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'

    def test(self, socket):
        socket.getfqdn = Mock(return_value='test')

        uk_tz = pytz.timezone('Europe/London')
        cali_tz = pytz.timezone('US/Pacific')
        nyc_tz = pytz.timezone('US/Eastern')

        start_utc = pytz.utc.localize(datetime(2000, 1, 1, 19))
        start_uk = uk_tz.localize(datetime(2000, 1, 1, 19))
        start_cali = cali_tz.localize(datetime(2000, 1, 1, 19))
        start_nyc = nyc_tz.localize(datetime(2000, 1, 1, 19))

        deadline_utc = pytz.utc.localize(datetime(2000, 1, 3, 0))
        deadline_uk = uk_tz.localize(datetime(2000, 1, 3, 0))
        deadline_cali = cali_tz.localize(datetime(2000, 1, 3, 0))
        deadline_nyc = nyc_tz.localize(datetime(2000, 1, 3, 0))

        uk_user = User.objects.create(email='uk@t.com', username='uk')
        uk_goal = Goal.objects.create(user=uk_user, text='test',
                                      timezone='Europe/London',
                                      start=start_uk)
        uk_goal.create_step('text', start_uk, commit=True)

        cali_user = User.objects.create(email='cali@t.com', username='cali')
        cali_goal = Goal.objects.create(user=cali_user, text='test',
                                        timezone='US/Pacific',
                                        start=start_cali)
        cali_goal.create_step('text', start_cali, commit=True)

        nyc_user = User.objects.create(email='nyc@t.com', username='nyc')
        nyc_goal = Goal.objects.create(user=nyc_user, text='test',
                                       timezone='US/Eastern',
                                       start=start_nyc)
        nyc_goal.create_step('text', start_nyc, commit=True)

        now = start_utc
        while now <= pytz.utc.localize(datetime(2000, 1, 8, 0)):
            # print(now)
            self.send_emails(now)

            # # # # uk # # # #

            if now == uk_tz.localize(datetime(2000, 1, 3, 0)):
                self.assertEmail(uk_goal, 'd1', 2)

            elif now == uk_tz.localize(datetime(2000, 1, 4, 0)):
                self.assertEmail(uk_goal, 'd2', 1)

            elif now == uk_tz.localize(datetime(2000, 1, 5, 0)):
                self.assertEmail(uk_goal, 'd3', 0)

            # # # # cali # # # #

            elif now == cali_tz.localize(datetime(2000, 1, 3, 0)):
                self.assertEmail(cali_goal, 'd1', 2)

            elif now == cali_tz.localize(datetime(2000, 1, 3, 19)):
                self.assertEquals(len(self.emails_sent), 0)
                self.track_step(cali_goal, now)

            elif now == cali_tz.localize(datetime(2000, 1, 5, 0)):
                self.assertEmail(cali_goal, 'd2', 1)

            elif now == cali_tz.localize(datetime(2000, 1, 5, 19)):
                self.assertEquals(len(self.emails_sent), 0)
                self.track_step(cali_goal, now)

            elif now == cali_tz.localize(datetime(2000, 1, 7, 0)):
                self.assertEmail(cali_goal, 'd3', 0)

            # # # # nyc # # # #

            elif now == nyc_tz.localize(datetime(2000, 1, 3, 0)):
                self.assertEmail(nyc_goal, 'd1', 2)

            elif now == nyc_tz.localize(datetime(2000, 1, 4, 0)):
                    self.assertEmail(nyc_goal, 'd2', 1)

            elif now == nyc_tz.localize(datetime(2000, 1, 5, 0)):
                self.assertEmail(nyc_goal, 'd3', 0)

            # # # # none # # # #

            else:
                self.assertEquals(len(self.emails_sent), 0)

            now += timedelta(minutes=15)

    def send_emails(self, now):
        self.emails_sent = send_d_emails_at_midnight(now)

    def track_step(self, goal, now):
        step = goal.steps.last()
        step.complete = True
        step.time_tracked = now
        step.save()

        next_step = goal.create_step('test', now, commit=True)

    def assertEmail(self, goal, name, lives):
        goal.refresh_from_db()

        msg = 'Expected %s email to %s' % (name, goal.user.email)

        self.assertEquals(len(self.emails_sent), 1, msg)

        email = self.emails_sent[0]

        self.assertEquals(email.recipient, goal.user, msg)
        self.assertEquals(email.name, name, msg)
        self.assertEquals(goal.lives, lives, msg)
