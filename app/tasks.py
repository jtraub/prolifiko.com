from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from celery import shared_task

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


@shared_task
def send_dr_emails():
    now = timezone.now()

    for user in dr_users(now, 24):
        send_email('dr1', user)

    for user in dr_users(now, 48):
        send_email('dr2', user)

    for user in dr_users(now, 72):
        send_email('dr3', user)


@shared_task
def send_d_emails():
    steps = Step.objects.filter(complete=False,
                                end__lt=timezone.now() - timedelta(hours=24))

    for step in steps:
        step.goal.lose_life(commit=True)

        if step.goal.lives == 2:
            send_email('d1', step.goal.user, {'step': step})

        if step.goal.lives == 1:
            send_email('d2', step.goal.user, {'step': step})

        if step.goal.lives == 0:
            send_email('d3', step.goal.user, {'step': step})
