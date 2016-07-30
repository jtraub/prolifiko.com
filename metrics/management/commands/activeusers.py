from django.core.management.base import BaseCommand, CommandError
from metrics.data import active_users


class Command(BaseCommand):
    help = 'Shows active users'

    def handle(self, *args, **options):
        users = active_users()

        print(len(users))
        for user in users:
            print(user.email)
