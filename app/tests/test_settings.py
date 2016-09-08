from django.test import TestCase
from unittest.mock import patch
import os
import importlib
from prolifiko.settings import base as settings


class TestSettings(TestCase):
    def test_default_email_settings(self):
        self.assertEquals(settings.EMAIL_SEND_PERIOD, 15)
        self.assertEquals(settings.EMAIL_SEND_PERIOD_UNIT, 'minutes')

    def test_environ_email_settings(self):
        environ = {
            'PF_EMAIL_SEND_PERIOD': '1',
            'PF_EMAIL_SEND_PERIOD_UNIT': 'minutes'
        }

        with patch.dict(os.environ, environ):
            importlib.reload(settings)

            self.assertEquals(settings.EMAIL_SEND_PERIOD, 1)
            self.assertEquals(settings.EMAIL_SEND_PERIOD_UNIT, 'minutes')
