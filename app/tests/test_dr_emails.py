from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from django.contrib.auth.models import User
from django.test import TestCase
import pytz
from app.tasks import send_dr_emails

import logging


@patch('django.core.mail.utils.socket')
class DrEmailTest(TestCase):
    def test(self, socket):
        socket.getfqdn = Mock(return_value='test')

        uk_tz = pytz.timezone('Europe/London')
        cali_tz = pytz.timezone('US/Pacific')
        nyc_tz = pytz.timezone('US/Eastern')

        register_utc = datetime(2000, 1, 1, 0).replace(tzinfo=pytz.utc)
        print('utc', register_utc)

        register_uk = uk_tz.localize(datetime(2000, 1, 1, 19))
        print('uk', register_uk.astimezone(pytz.utc))
        uk_user = User.objects.create(
            email='uk@dr.com', username='uk_dr', date_joined=register_uk)

        register_cali = cali_tz.localize(datetime(2000, 1, 1, 19))
        print('cali', register_cali.astimezone(pytz.utc))
        cali_user = User.objects.create(
            email='cali@dr.com', username='cali_dr', date_joined=register_cali)

        register_nyc = nyc_tz.localize(datetime(2000, 1, 1, 19))
        print('nyc', register_nyc.astimezone(pytz.utc))
        nyc_user = User.objects.create(
            email='nyc@dr.com', username='nyc_dr', date_joined=register_nyc)

        now = register_utc
        while now <= pytz.utc.localize(datetime(2000, 1, 5, 0)):
            self.send_emails(now)

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

            now += timedelta(minutes=15)

    def send_emails(self, now):
        self.emails_sent = send_dr_emails(now)

    def assertEmail(self, user, name):
        msg = 'Expected %s email to %s' % (name, user.email)

        self.assertEquals(len(self.emails_sent), 1, msg)

        email = self.emails_sent[0]

        self.assertEquals(email.recipient, user, msg)
        self.assertEquals(email.name, name, msg)
