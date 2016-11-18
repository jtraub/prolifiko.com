from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta, datetime
from celery import shared_task
import pytz

from app.subscriptions import is_user_subscribed
from .utils import send_email
from .models import Email, Step, Goal

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def send_dr_emails(now=None):
    if now is None:
        now = timezone.now()

    logger.info('Sending DR emails')

    emails_sent = []

    def dr_users(more_than, less_than=None):
        before = now - more_than

        if less_than is not None:
            after = now - less_than
        else:
            after = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)

        logger.info('Looking for users where %s >= date joined > %s' %
                    (before, after))

        return User.objects \
            .annotate(goal_count=Count('goal')) \
            .annotate(subscription_count=Count('subscription')) \
            .filter(is_active=True) \
            .filter(date_joined__lte=before, date_joined__gt=after) \
            .filter(goal_count=0) \
            .filter(subscription_count=0)

    def send_dr_email(recipient, name):
        dr_emails_sent = [email.name for email in
                          Email.objects.filter(recipient=recipient).all()
                          if email.type == Email.TYPE_DR]

        if name not in dr_emails_sent:
            msg = 'Found user %s who registered more than %s ago ' + \
                  'and has received %s emails; sending %s'
            logger.info(msg % (recipient.email, now - recipient.date_joined,
                               dr_emails_sent, name))

            emails_sent.append(send_email(name, recipient))

    for user in dr_users(timedelta(hours=24), timedelta(hours=48)):
        send_dr_email(user, 'dr1')

    for user in dr_users(timedelta(hours=48), timedelta(hours=72)):
        send_dr_email(user, 'dr2')

    for user in dr_users(timedelta(hours=72)):
        send_dr_email(user, 'dr3')

    return emails_sent


@shared_task
def send_d_emails_at_midnight(now=None):
    logger.info('Sending D email')

    if now is None:
        now = timezone.now()

    emails_sent = []

    logger.info('Looking for late steps where deadline <= %s' % now)

    late_steps = Step.objects.filter(goal__user__is_active=True,
                                     goal__type=Goal.TYPE_FIVE_DAY,
                                     goal__deleted=False,
                                     goal__lives__gt=0,
                                     goal__complete=False,
                                     complete=False,
                                     deadline__lte=now)

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
