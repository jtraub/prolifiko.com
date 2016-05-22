from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from .utils import send_email, get_logger
from .models import Step


logger = get_logger(__name__)


def dr_users(now, hours):
    before = now - timedelta(hours=hours)
    after = before - timedelta(hours=24)

    return User.objects \
        .annotate(goal_count=Count('goal')) \
        .filter(date_joined__lt=before, date_joined__gt=after) \
        .filter(goal_count=0)


def send_dr_emails(self):
    now = timezone.now()

    for user in dr_users(now, 24):
        send_email('dr1', user)

    for user in dr_users(now, 48):
        send_email('dr2', user)

    for user in dr_users(now, 72):
        send_email('dr3', user)


def send_d_emails(self):
    pass
