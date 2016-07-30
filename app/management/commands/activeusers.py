from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db.models import Q
from app.models import Email


class Command(BaseCommand):
    help = 'Shows active users'

    def handle(self, *args, **options):
        test_users = User.objects.filter(is_active=True, is_staff=False) \
            .filter(date_joined__gte='2016-07-17') \
            .filter(date_joined__lte='2016-07-26')

        active_users = [
            user for user in test_users if
            Email.objects.filter(recipient=user)
                         .filter(Q(name='dr3') | Q(name='d3'))
                         .count() > 0
        ]

        print(len(active_users))
        for user in active_users:
            print(user.email)
