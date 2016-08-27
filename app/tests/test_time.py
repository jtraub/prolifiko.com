from datetime import datetime, timedelta, time
from django.test import TestCase
from django.utils.timezone import is_aware
import pytz
from app.models import Step


class TimeTest(TestCase):
    def test_deadline(self):
        # Hong Kong UTC+8 - doesn't observe DST
        tz = pytz.timezone('Asia/Hong_Kong')

        start = tz.localize(datetime.utcnow())

        deadline = Step.deadline(start, 'Asia/Hong_Kong')

        self.assertTrue(is_aware(deadline))
        self.assertEquals(deadline.tzinfo, pytz.utc)

        local_deadline = deadline.astimezone(tz)
        print(deadline, local_deadline)
        self.assertEquals(start.date() + timedelta(days=2),
                          local_deadline.date())
        self.assertEquals(local_deadline.time(), time())
