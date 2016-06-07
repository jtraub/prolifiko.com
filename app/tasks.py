from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from celery import shared_task

from .utils import send_email, get_logger
from .models import Goal, Email, Step

DELTA = {settings.INACTIVE_TIME_UNIT: settings.INACTIVE_TIME}


@shared_task
def send_dr_emails():
    logger = get_logger(__name__ + '.send_dr_emails')

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
    logger = get_logger(__name__ + '.send_d_emails')

    logger.info('Sending D emails')

    now = timezone.now()
    delta = timedelta(**DELTA)
    deadline = now - delta

    steps = Step.objects.filter(complete=False,
                                end__lte=deadline,
                                goal__lives__gt=0)

    email_progression = ('d1', 'd2', 'd3')

    for step in steps:
        goal = step.goal
        user = goal.user

        logger.debug('Found late step %s for %s' % (step.id, user.email))

        sent_emails = list(email for email in
                           Email.objects.filter(recipient=user).all()
                           if email.type == Email.TYPE_D)

        if len(sent_emails) == 0:
            logger.debug('No emails sent to %s; sending D1' % user.email)
            goal.lose_life()
            email = send_email('d1', user, {'step': step})
            email.step = step
            email.save()

            break

        logger.debug('Already sent %s emails to %s' % (
            [email.name for email in sent_emails], user.email))

        if len(sent_emails) >= 3:
            logger.debug('All D emails sent to %s; stopping' % user.email)
            break

        previous_email = sent_emails[-1] if len(sent_emails) > 1 \
            else sent_emails[0]

        logger.debug('Last email sent to %s was %s at %s' % (
            user.email, previous_email.name, previous_email.sent
        ))

        if previous_email.sent + delta < now:
            goal.lose_life()

            next_email = email_progression[len(sent_emails)]

            email = send_email(next_email, user, {'step': step})
            email.step = step
            email.save()
        else:
            logger.debug('%s not ready for next email; stopping' % user.email)
