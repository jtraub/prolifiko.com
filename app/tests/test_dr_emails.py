from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from freezegun import freeze_time
import pytz

from app.models import Subscription
from app.tasks import send_dr_emails


@override_settings(DEBUG=True)
@patch('django.core.mail.utils.socket')
class DrEmailTest(TestCase):
    def test(self, socket):
        socket.getfqdn = Mock(return_value='test')

        uk_tz = pytz.timezone('Europe/London')
        cali_tz = pytz.timezone('US/Pacific')
        nyc_tz = pytz.timezone('US/Eastern')

        register_utc = datetime(2000, 1, 1, 0).replace(tzinfo=pytz.utc)

        register_uk = uk_tz.localize(datetime(2000, 1, 1, 19))
        uk_user = User.objects.create(
            email='uk@dr.com', username='uk_dr', date_joined=register_uk)

        register_cali = cali_tz.localize(datetime(2000, 1, 1, 19))
        cali_user = User.objects.create(
            email='cali@dr.com', username='cali_dr', date_joined=register_cali)

        register_nyc = nyc_tz.localize(datetime(2000, 1, 1, 19))
        nyc_user = User.objects.create(
            email='nyc@dr.com', username='nyc_dr', date_joined=register_nyc)

        # Add a subscribed user to check they don't get any emails
        subscribed_user = User.objects.create(
            email='sub@dr.com', username='sub_dr', date_joined=register_uk)
        Subscription.objects.create(user=subscribed_user, name='test')

        with freeze_time(register_utc) as frozen_now:
            while datetime.now(tz=pytz.utc) <= \
                  pytz.utc.localize(datetime(2000, 1, 5, 0)):

                self.send_emails()
                now = datetime.now(tz=pytz.utc)

                # # # # dr1 # # # #
                if now == uk_tz.localize(datetime(2000, 1, 2, 19)):
                    self.assertEmail(uk_user, 'dr1')
                elif now == cali_tz.localize(datetime(2000, 1, 2, 19)):
                    self.assertEmail(cali_user, 'dr1')
                elif now == nyc_tz.localize(datetime(2000, 1, 2, 19)):
                    self.assertEmail(nyc_user, 'dr1')

                # # # # dr2 # # # #
                elif now == uk_tz.localize(datetime(2000, 1, 3, 19)):
                    self.assertEmail(uk_user, 'dr2')
                elif now == cali_tz.localize(datetime(2000, 1, 3, 19)):
                    self.assertEmail(cali_user, 'dr2')
                elif now == nyc_tz.localize(datetime(2000, 1, 3, 19)):
                    self.assertEmail(nyc_user, 'dr2')

                # # # # dr3 # # # #
                elif now == uk_tz.localize(datetime(2000, 1, 4, 19)):
                    self.assertEmail(uk_user, 'dr3')
                elif now == cali_tz.localize(datetime(2000, 1, 4, 19)):
                    self.assertEmail(cali_user, 'dr3')
                elif now == nyc_tz.localize(datetime(2000, 1, 4, 19)):
                    self.assertEmail(nyc_user, 'dr3')

                else:
                    self.assertEquals(len(self.emails_sent), 0, now)

                frozen_now.tick(delta=timedelta(minutes=15))

    def send_emails(self):
        self.emails_sent = send_dr_emails()

    def assertEmail(self, user, name):
        msg = 'Expected %s email to %s' % (name, user.email)

        self.assertEquals(len(self.emails_sent), 1, msg)

        email = self.emails_sent[0]

        self.assertEquals(email.recipient, user, msg)
        self.assertEquals(email.name, name, msg)
