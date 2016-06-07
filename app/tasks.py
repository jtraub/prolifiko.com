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

    now = timezone.now()
    delta = timedelta(**DELTA)
    deadline = now - delta

    goals = Goal.objects.filter(complete=False,
                                steps__complete=False,
                                steps__end__lte=deadline,
                                lives__gt=0)

    email_progression = ('d1', 'd2', 'd3')

    for goal in goals:
        current_step = goal.current_step

        sent_emails = list(Email.objects.filter(recipient=goal.user))

        if len(sent_emails) == 0:
            goal.lose_life()
            email = send_email('d1', goal.user, {'step': current_step})
            email.step = current_step
            email.save()

            break

        if len(sent_emails) >= 3:
            break

        previous_email = sent_emails[-1] if len(sent_emails) > 1 \
            else sent_emails[0]

        if previous_email.sent + delta < now:
            goal.lose_life()

            d_emails_sent = len([email for email in sent_emails
                                if email.type == Email.TYPE_D])

            if d_emails_sent > 2:
                break

            next_email = email_progression[d_emails_sent]

            email = send_email(next_email, goal.user, {'step': current_step})
            email.step = current_step
            email.save()
