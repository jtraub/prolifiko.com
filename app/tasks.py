from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from celery import shared_task

from .utils import send_email, get_logger
from .models import Goal, Email, Step


logger = get_logger(__name__)

DELTA = {settings.INACTIVE_TIME_UNIT: settings.INACTIVE_TIME}


@shared_task
def send_dr_emails():
    logger.info('Sending DR emails')

    now = timezone.now()

    def dr_users(delta):
        before = now - timedelta(**{settings.INACTIVE_TIME_UNIT: delta})
        after = before - timedelta(**DELTA)

        return User.objects \
            .annotate(goal_count=Count('goal')) \
            .filter(date_joined__lt=before, date_joined__gt=after) \
            .filter(goal_count=0)

    for name, multiplier in (('dr1', 1), ('dr2', 2), ('dr3', 3)):
        for user in dr_users(settings.INACTIVE_TIME * multiplier):
            email_names = [email.name for email in
                           Email.objects.filter(recipient=user).all()]

            if name not in email_names:
                send_email(name, user)


@shared_task
def send_d_emails():
    logger.info('Sending D emails')

    deadline = timezone.now() - timedelta(**DELTA)

    goals = Goal.objects.filter(complete=False,
                                steps__complete=False,
                                steps__end__lte=deadline,
                                lives__gt=0)

    for goal in goals:
        goal.lose_life(commit=True)
        email_names = [email.name for email in
                       Email.objects.filter(recipient=goal.user)]

        for lives, email in ((2, 'd1'), (1, 'd2'), (0, 'd3')):
            if goal.lives == lives and email not in email_names:
                send_email(email, goal.user, {'step': goal.current_step})
