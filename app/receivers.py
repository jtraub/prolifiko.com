from django.dispatch import receiver
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

    add_event('register', {
        'id': user.id,
        'email': user.email
    })

    send_email('n1_registration', user)


@receiver(new_goal)
@log_signal
def receive_new_goal(sender, **kwargs):
    goal = kwargs['goal']

    add_event('goals.new', {
        'id': goal.id.hex,
        'user_id': goal.user.id
    })


@receiver(new_step)
@log_signal
def receive_new_step(sender, **kwargs):
    step = kwargs['step']

    add_event('steps.new', {
        'id': step.id.hex,
        'user_id': step.goal.user.id,
        'goal_id': step.goal.id.hex
    })

    if step.goal.steps.count() == 1:
        send_email('n2_new_goal', step.goal.user, {
            'first_step': step
        })
    else:
        # We want the step before this one - that's the one that's been
        # completed. E.g. if we've received step 2 here, we want step_num to be
        # 1, which is the list index of step 2.
        step_num = list(step.goal.steps.all()).index(step)
        n_num = step_num + 2
        send_email('n%d_step_%d_complete' % (n_num, step_num), step.goal.user,
                   {'next_step': step})


@receiver(step_complete)
@log_signal
def receive_step_complete(sender, **kwargs):
    step = kwargs['step']

    add_event('steps.track', {
        'id': step.id.hex,
        'user_id': step.goal.user.id,
        'goal_id': step.goal.id.hex
    })
