from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from django.test import TestCase, override_settings
from freezegun import freeze_time
import pytz
from app import fixtures
from app.tasks import send_d_emails_at_midnight


@override_settings(DEBUG=True)
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

        uk_user = fixtures.user('uk@d.com', 'Europe/London', subscribed=False)
        uk_goal = fixtures.five_day_challenge(uk_user, start=start_uk)
        fixtures.step(uk_goal, start=start_uk)

        cali_user = fixtures.user('cali@d.com', 'US/Pacific', subscribed=False)
        cali_goal = fixtures.five_day_challenge(cali_user, start=start_cali)
        fixtures.step(cali_goal, start=start_cali)

        nyc_user = fixtures.user('nyc@d.com', 'US/Eastern', subscribed=False)
        nyc_goal = fixtures.five_day_challenge(nyc_user, start=start_nyc)
        fixtures.step(nyc_goal, start=start_nyc)

        # Add a subscribed user to check they don't get any emails
        subscribed_user = fixtures.user('sub@d.com', 'Europe/London')
        subscribed_goal = fixtures.goal(subscribed_user, start=start_uk)
        fixtures.step(subscribed_goal, start=start_uk)

        with freeze_time(start_utc) as frozen_now:
            while datetime.now(tz=pytz.utc) <= \
                  pytz.utc.localize(datetime(2000, 1, 8, 0)):

                self.send_emails()
                now = datetime.now(tz=pytz.utc)

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

                frozen_now.tick(delta=timedelta(minutes=15))

    def send_emails(self):
        self.emails_sent = send_d_emails_at_midnight()

    def track_step(self, goal, now):
        step = goal.steps.last()
        step.complete = True
        step.time_tracked = now
        step.save()

        fixtures.step(goal, start=now)

    def assertEmail(self, goal, name, lives):
        goal.refresh_from_db()

        msg = 'Expected %s email to %s' % (name, goal.user.email)

        self.assertEquals(len(self.emails_sent), 1, msg)

        email = self.emails_sent[0]

        self.assertEquals(email.recipient, goal.user, msg)
        self.assertEquals(email.name, name, msg)
        self.assertEquals(goal.lives, lives, msg)
