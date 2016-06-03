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

    print('now', now)
    print('deadline', deadline)

    goals = Goal.objects.filter(complete=False,
                                steps__complete=False,
                                steps__end__lte=deadline,
                                lives__gt=0)

    email_progression = ('d1', 'd2', 'd3')

    for goal in goals:
        print('goal user=%s lives=%d' % (goal.user.email, goal.lives))

        current_step = goal.current_step

        print('step.end', current_step.end)

        sent_emails = list(Email.objects.filter(recipient=goal.user))

        print('sent_emails', [email.name for email in sent_emails])

        if len(sent_emails) == 0:
            goal.lose_life()
            print('send to=%s name=d1' % goal.user.email)
            email = send_email('d1', goal.user, {'step': current_step})
            email.step = current_step
            email.save()

            break

        if len(sent_emails) >= 3:
            break

        previous_email = sent_emails[-1] if len(sent_emails) > 1 \
            else sent_emails[0]

        print('previous email', previous_email)
        print('previous_email name=%s sent=%s deadline=%s' %
              (previous_email.name,
               previous_email.sent,
               previous_email.sent + delta))

        if previous_email.sent + delta < now:
            goal.lose_life()

            dr_emails_sent = len([email for email in sent_emails
                                  if email.type == Email.TYPE_DR])
            d_emails_sent = len([email for email in sent_emails
                                 if email.type == Email.TYPE_D])

            print('dr_emails_sent', dr_emails_sent)
            print('d_emails_sent', d_emails_sent)

            next_email_pos = dr_emails_sent + d_emails_sent

            if next_email_pos > 2:
                break

            next_email = email_progression[next_email_pos]

            print('send to=%s name=%s' % (goal.user.email, next_email))
            email = send_email(next_email, goal.user, {'step': current_step})
            email.step = current_step
            email.save()
