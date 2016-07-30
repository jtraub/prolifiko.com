from django.core.management.base import BaseCommand, CommandError
import sys
from app.models import Goal, Email
from metrics.data import real_users
import csv


class Command(BaseCommand):
    help = 'Shows active users'

    def handle(self, *args, **options):
        writer = csv.writer(sys.stdout)

        names = ['DR1', 'DR2', 'DR3', 'D1', 'D2', 'D3']
        writer.writerow(['Email'] + names)

        for user in real_users():
            row = [
                user.email,
            ]

            for name in names:
                email = Email.objects.filter(recipient=user) \
                    .filter(name=name.lower()) \
                    .first()

                if email:
                    row.append(email.sent)
                else:
                    row.append('')

            writer.writerow(row)
