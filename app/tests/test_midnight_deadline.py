from datetime import datetime, date, time
import pytz
from app.models import Step


def test_midnight_deadline_uk():
    uk_tz = pytz.timezone('Europe/London')
    uk_start = datetime(2016, 1, 1, 19, 0).replace(tzinfo=uk_tz)

    uk_deadline = Step.midnight_deadline(uk_start, uk_tz)

    assert uk_deadline == datetime(2016, 1, 3, 0, 0) \
        .replace(tzinfo=uk_tz).astimezone(pytz.utc)


def test_midnight_deadline_nyc():
    nyc_tz = pytz.timezone('US/Eastern')
    nyc_start = datetime(2016, 1, 1, 19, 0).replace(tzinfo=nyc_tz)

    nyc_deadline = Step.midnight_deadline(nyc_start, nyc_tz)

    assert nyc_deadline == datetime(2016, 1, 3, 0, 0) \
        .replace(tzinfo=nyc_tz).astimezone(pytz.utc)
