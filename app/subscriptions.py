from app.models import Subscription


def is_user_subscribed(user):
    return user.is_authenticated() and \
           Subscription.objects.filter(user=user).count() > 0
