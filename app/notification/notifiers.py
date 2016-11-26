from app.models import Step
from app.utils import send_email


def email_late_step(item, *args):
    if not(isinstance(item, Step)):
        return
    goal = item.goal
    user = goal.user
    email_to_send = 'd{}'.format(4 - goal.lives)

    return send_email(email_to_send, user, goal)


def email_dr_notifier(user, *args, name=None):
    return send_email(name, user)


def email_dr1_notifier(user, *args):
    return email_dr_notifier(user, *args, name='dr1')


def email_dr2_notifier(user, *args):
    return email_dr_notifier(user, *args, name='dr2')


def email_dr3_notifier(user, *args):
    return email_dr_notifier(user, *args, name='dr3')
