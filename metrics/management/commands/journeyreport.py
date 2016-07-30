from django.core.management.base import BaseCommand, CommandError
import sys
from app.models import Goal
from metrics.data import real_users
import csv


class Command(BaseCommand):
    help = 'Shows active users'

    def handle(self, *args, **options):
        writer = csv.writer(sys.stdout)

        writer.writerow([
            'Email', 'Registration', 'New Goal', 'Step #1', 'Track #1',
            'Step #2', 'Track #2', 'Step #3', 'Track #3', 'Step #4',
            'Track #4', 'Step #5', 'Track #5'
        ])

        for user in real_users():
            row = [
                user.email,
                user.date_joined
            ]

            goal = Goal.objects.filter(user=user).first()

            if goal:
                row.append(goal.start)

                for step in goal.steps.all():
                    row.append(step.start)
                    row.append(step.time_tracked)

            writer.writerow(row)
