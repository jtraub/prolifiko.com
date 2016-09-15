from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from celery import shared_task

from .utils import send_email
from .models import Email, Step, Goal

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def send_dr_emails(now=None, inactive=None):
    if now is None:
        now = timezone.now()

    if inactive is None:
        inactive = timedelta(hours=24)

    logger.info('Sending DR emails')

    now = timezone.now()

    def dr_users(delta):
        before = now - delta
        after = before - inactive

        return User.objects \
            .annotate(goal_count=Count('goal')) \
            .filter(is_active=True) \
            .filter(date_joined__lt=before, date_joined__gt=after) \
            .filter(goal_count=0)

    for name, multiplier in (('dr1', 1), ('dr2', 2), ('dr3', 3)):
        for user in dr_users(inactive):
            sent_emails = [email.name for email in
                           Email.objects.filter(recipient=user).all()
                           if email.type == Email.TYPE_DR]

            if name not in sent_emails:
                msg = 'Found user %s who registered more than %s ago ' + \
                      'and has received %s emails; sending %s'
                logger.debug(msg % (user.email, inactive, sent_emails, name))

                send_email(name, user)


@shared_task
def send_d_emails_at_midnight(now=None):
    if now is None:
        now = timezone.now()

    emails_sent = []

    late_steps = Step.objects.filter(goal__user__is_active=True,
                                     goal__deleted=False,
                                     goal__lives__gt=0,
                                     goal__complete=False,
                                     complete=False,
                                     end__lte=now)

    for step in late_steps:
        goal = step.goal
        user = goal.user

        # 3 lives = d1
        # 2 lives = d2
        # 1 life = d3
        email_to_send = 'd%d' % (4 - goal.lives)

        logger.info('Sending %s to %s step=%s goal=%s' % (
            email_to_send, user.email, step.id, goal.id))
        with transaction.atomic():
            step.lose_life(now)

            email = send_email(email_to_send, user, goal)
            email.step = step
            email.save()

        emails_sent.append(email)

    return emails_sent
