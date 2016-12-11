from datetime import timedelta, datetime
from celery import shared_task

from app.notification import notify, callbacks, rules, notifiers, filters
from functools import partial

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def send_dr_emails():
    logger.info('Sending DR emails')

    joined_users = rules.joined_users
    joined_users_24_48 = partial(joined_users, timedelta(hours=24),
                                 timedelta(hours=48))
    joined_users_48_72 = partial(joined_users, timedelta(hours=48),
                                 timedelta(hours=72))
    joined_users_72 = partial(joined_users, timedelta(hours=72))

    rules_ = [joined_users_24_48, joined_users_48_72, joined_users_72]
    notifiers_ = [notifiers.email_dr1_notifier, notifiers.email_dr2_notifier,
                  notifiers.email_dr3_notifier]
    filters_ = [filters.not_sent_dr1_email, filters.not_sent_dr2_email,
                filters.not_sent_dr3_email]

    results = []
    for r, n, f in zip(rules_, notifiers_, filters_):
        results.extend(notify(rule=r, notifiers=n, filters=f))

    return results


@shared_task
def send_d_emails_at_midnight():
    logger.info('Sending D email')
    return notify(
        rule=rules.late_steps,
        filters=filters.not_subscribed_user,
        notifiers=notifiers.email_late_step,
        success=callbacks.late_step_success
    )


@shared_task
def send_r_emails():
    logger.info('Sending R email')
    return notify(
        rule=rules.upcoming_step_deadlines,
        filters=filters.not_subscribed_user,
        notifiers=notifiers.email_r_notifier,
    )
