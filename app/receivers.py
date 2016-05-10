from django.dispatch import receiver
from .signals import *
from .utils import send_email, add_event


@receiver(new_goal)
def receive_new_goal(sender, **kwargs):
    goal = kwargs['goal']

    add_event('goals.new', {
        'id': goal.id.hex,
        'user_id': goal.user.id
    })


@receiver(step_complete)
def receive_step_complete(sender, **kwargs):
    step = kwargs['step']

    add_event('steps.track', {
        'id': step.id.hex,
        'user_id': step.goal.user.id,
        'goal_id': step.goal.id.hex
    })

    step_num = list(step.goal.steps.all()).index(step) + 1
    send_email('step_%d_complete' % step_num, step.goal.user, {
        'goal': step.goal
    })


@receiver(new_step)
def receive_new_step(sender, **kwargs):
    step = kwargs['step']

    add_event('steps.new', {
        'id': step.id.hex,
        'user_id': step.goal.user.id,
        'goal_id': step.goal.id.hex
    })

    if step.goal.steps.count() == 1:
        send_email('new_goal', step.goal.user, {
            'goal': step.goal
        })

