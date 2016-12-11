from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models import Count, Sum, When, Case, IntegerField
from django.utils import timezone
import pytz

from app.models import Step, Goal


def late_steps():
    now = timezone.now()
    return Step.objects.filter(goal__user__is_active=True,
                               goal__type=Goal.TYPE_FIVE_DAY,
                               goal__deleted=False,
                               goal__lives__gt=0,
                               goal__complete=False,
                               complete=False,
                               deadline__lte=now)


def upcoming_step_deadlines():
    now = timezone.now()
    twelve_hrs = timedelta(hours=12)
    upcoming_deadline = now + twelve_hrs
    return Step.objects.filter(goal__user__is_active=True,
                               goal__type=Goal.TYPE_FIVE_DAY,
                               goal__deleted=False,
                               goal__lives__gt=0,
                               goal__complete=False,
                               complete=False,
                               deadline__lte=upcoming_deadline,
                               deadline__gte=now) \
        .annotate(num_r_emails=Sum(
            Case(
                When(emails__name='r',
                     emails__sent__gte=(now -
                                        (timedelta(hours=24) - twelve_hrs)),
                     then=1),
                default=0, output_field=IntegerField()
            )
        )).filter(num_r_emails=0).distinct()


def joined_users(more_than, less_than=None):
    now = timezone.now()
    before = now - more_than

    if less_than is not None:
        after = now - less_than
    else:
        after = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)

    return User.objects \
        .annotate(goal_count=Count('goal')) \
        .annotate(subscription_count=Count('subscription')) \
        .filter(is_active=True) \
        .filter(date_joined__lte=before, date_joined__gt=after) \
        .filter(goal_count=0) \
        .filter(subscription_count=0)
