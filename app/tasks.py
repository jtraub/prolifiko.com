from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from celery import shared_task
import pytz

from .utils import send_email
from .models import Email, Step, Goal

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def send_dr_emails():
    logger.info('Sending DR emails')

    now = timezone.now()

    def dr_users(_delta):
        before = now - _delta
        after = before - settings.INACTIVE_DELTA

        return User.objects \
            .annotate(goal_count=Count('goal')) \
            .filter(is_active=True) \
            .filter(date_joined__lt=before, date_joined__gt=after) \
            .filter(goal_count=0)

    for name, multiplier in (('dr1', 1), ('dr2', 2), ('dr3', 3)):
        delta = timedelta(**{
            settings.INACTIVE_TIME_UNIT: settings.INACTIVE_TIME * multiplier
        })

        for user in dr_users(delta):
            sent_emails = [email.name for email in
                           Email.objects.filter(recipient=user).all()
                           if email.type == Email.TYPE_DR]

            if name not in sent_emails:
                msg = 'Found user %s who registered more than %s ago ' + \
                      'and has received %s emails; sending %s'
                logger.debug(msg % (user.email, delta, sent_emails, name))

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

        with transaction.atomic():
            step.lose_life(now)

            email = send_email(email_to_send, user, goal)
            email.step = step
            email.save()

        emails_sent.append(email)

    return emails_sent


@shared_task
def send_d_emails():
    logger.info('Sending D emails')

    now = timezone.now()

    logger.debug('Looking for incomplete steps with an end time before %s'
                 % now)

    late_steps = Step.objects \
        .filter(goal__lives__gt=0, goal__user__is_active=True) \
        .filter(complete=False, end__lte=now,)

    for step in late_steps:
        logger.debug('Found late step user=%s step=%s overdue=%s end=%s' % (
            step.user.email, step.number, now - step.end, step.end
        ))

    logger.debug('Looking for inactive goals where ' +
                 'latest step tracked before %s' %
                 (now - settings.INACTIVE_DELTA))
    inactive_goals = []

    for goal in Goal.objects \
            .annotate(step_count=Count('steps')) \
            .filter(user__is_active=True) \
            .filter(active=False, complete=False, step_count__gt=0):

        if goal.current_step.time_tracked < now - settings.INACTIVE_DELTA:
            logger.debug('Found inactive goal user=%s' % goal.user.email)

            inactive_goals.append(goal.current_step)

    email_progression = ('d1', 'd2', 'd3')

    for step in list(late_steps) + inactive_goals:
        logger.debug('Checking step user=%s step=%s overdue=%s end=%s' % (
            step.user.email, step.number, now - step.end, step.end
        ))

        goal = step.goal
        user = goal.user

        sent_emails = list(email for email in
                           Email.objects.filter(recipient=user).all()
                           if email.type == Email.TYPE_D)

        if len(sent_emails) == 0:
            logger.debug('No emails sent to %s; sending D1' % user.email)
            goal.lose_life()
            email = send_email('d1', user, goal)
            email.step = step
            email.save()

            continue

        logger.debug('Already sent %s emails to %s' % (
            [email.name for email in sent_emails], user.email))

        if len(sent_emails) >= 3:
            logger.debug('All D emails sent to %s; stopping' % user.email)
            continue

        previous_email = sent_emails[-1] if len(sent_emails) > 1 \
            else sent_emails[0]

        logger.debug('Last email sent to %s was %s at %s' % (
            user.email, previous_email.name, previous_email.sent
        ))

        if previous_email.sent + settings.INACTIVE_DELTA < now:
            goal.lose_life()

            next_email = email_progression[len(sent_emails)]

            logger.debug('Sending %s to %s; goal now has %d lives' %
                         (next_email, goal.user, goal.lives))

            email = send_email(next_email, user, goal)
            email.step = step
            email.save()
        else:
            logger.debug('%s not ready for next email; stopping' % user.email)
