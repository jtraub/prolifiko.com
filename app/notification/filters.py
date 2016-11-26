from app.models import Email
from app.subscriptions import is_user_subscribed


def not_subscribed_user(item):
    goal = item.goal
    user = goal.user
    return not(is_user_subscribed(user))


def not_sent_email(recipient, name=''):
    dr_emails_sent = [email.name for email in
                      Email.objects.filter(recipient=recipient).all()
                      if email.type == Email.TYPE_DR]

    if name not in dr_emails_sent:
        return True

    return False


def not_sent_dr1_email(recipient):
    return not_sent_email(recipient, name='dr1')


def not_sent_dr2_email(recipient):
    return not_sent_email(recipient, name='dr2')


def not_sent_dr3_email(recipient):
    return not_sent_email(recipient, name='dr3')
