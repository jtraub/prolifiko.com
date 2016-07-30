from functools import reduce
import operator
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
from app.models import Email, Goal
from datetime import date


def real_users():
    email_domains = reduce(operator.or_, (
        Q(email__endswith=domain)
        for domain in settings.TEST_EMAIL_DOMAINS))

    return User.objects.filter(is_staff=False) \
        .exclude(email__in=settings.TEST_EMAIL_ADDRESSES) \
        .exclude(email_domains) \
        .order_by('email')


def active_users(start=date(2016, 7, 17), end=date(2016, 7, 26)):
    # Joined during test dates and have not deactivated
    test_users = real_users() \
        .filter(is_active=True) \
        .filter(date_joined__gte=start) \
        .filter(date_joined__lte=end)

    # Have an active goal
    users_with_active_goals = [
        user for user in test_users if
        Goal.objects.filter(user=user, complete=False)
    ]

    # Have not been sent DR3 or D3
    return [
        user for user in users_with_active_goals if
        Email.objects.filter(recipient=user)
                     .filter(Q(name='dr3') | Q(name='d3'))
                     .count() == 0
        ]
