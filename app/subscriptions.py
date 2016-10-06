from app.models import Subscription


def is_user_subscribed(user):
    return Subscription.objects.filter(user=user).count() > 0
