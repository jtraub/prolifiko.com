from django.dispatch import receiver

from app.models import Goal, Subscription, Timezone
from app.subscriptions import is_user_subscribed
from .signals import *
from .utils import send_email, add_event, get_logger

logger = get_logger(__name__)


def log_signal(func):
    def log(sender, **kwargs):
        if isinstance(sender, str):
            sender_name = sender
        elif hasattr(sender, '__name__'):
            sender_name = sender.__name__
        elif hasattr(sender, '__class__'):
            sender_name = sender.__class__.__name__
        else:
            sender_name = 'unknown'

        signal_name = func.__name__[8:]

        logger.debug('Received %s signal from %s %s' % (
            signal_name, sender_name, str(kwargs)))

        func(sender, **kwargs)

    return log


@receiver(registration)
@log_signal
def receive_registration(sender, **kwargs):
    user = kwargs['user']

    add_event('register', user, {
        'subscribed': is_user_subscribed(user),
        'timezone': Timezone.objects.get(user=user).name
    })

    send_email('n1_registration', user)


@receiver(registration)
@log_signal
def receive_registration(sender, **kwargs):
    user = kwargs['user']

    add_event('register', user, {
        'timezone': Timezone.objects.get(user=user).name
    })

    if is_user_subscribed(user):
        add_event('subscribe', user)


@receiver(new_goal)
@log_signal
def receive_new_goal(sender, **kwargs):
    goal = kwargs['goal']

    add_event('goals.new', goal.user, {
        'goal_id': goal.id.hex,
        'goal_type': goal.type
    })

    if goal.is_five_day:
        send_email('n2_new_goal', goal.user, goal)
    else:
        if Goal.objects.filter(user=goal.user).count() == 1:
            send_email('new_custom_goal', goal.user, goal)


@receiver(goal_complete)
@log_signal
def receive_goal_complete(send, **kwargs):
    goal = kwargs['goal']

    add_event('goals.complete', goal.user, {
        'goal_id': goal.id.hex,
        'goal_type': goal.type
    })

    if goal.is_five_day:
        send_email('n7_goal_complete', goal.user, goal)


@receiver(new_step)
@log_signal
def receive_new_step(sender, **kwargs):
    step = kwargs['step']

    add_event('steps.new', step.goal.user, {
        'goal_id': step.goal.id.hex,
        'goal_type': step.goal.type,
        'step_id': step.id.hex,
        'step_num': step.number
    })

    if step.goal.is_five_day and step.number > 1:
        # We want the step before this one - that's the one that's been
        # completed. E.g. if we've received step 2 here, we want step
        # num to be 1, which is the list index of step 2.
        step_num = step.number - 1
        n_num = step_num + 2
        email = 'n%d_step_%d_complete' % (n_num, step_num)
        send_email(email, step.goal.user, step.goal)


@receiver(step_complete)
@log_signal
def receive_step_complete(sender, **kwargs):
    step = kwargs['step']

    add_event('steps.complete', step.goal.user, {
        'goal_id': step.goal.id.hex,
        'goal_type': step.goal.type,
        'step_id': step.id.hex,
        'step_num': step.number
    })


@receiver(email)
@log_signal
def receive_email(sender, **kwargs):
    email_sent = kwargs['email']

    add_event('email', email_sent.recipient, {
        'email_name': email_sent.name
    })
