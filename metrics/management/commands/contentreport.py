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
            'Email', 'Goal', 'Step 1', 'Progress 1', 'Step 2', 'Progress 2',
            'Step 3', 'Progress 3', 'Step 4', 'Progress 4', 'Step 5',
            'Progress 5'
        ])

        for user in real_users():
            row = [
                user.email,
            ]

            goal = Goal.objects.filter(user=user).first()

            if goal:
                row.append(goal.text)

                for step in goal.steps.all():
                    row.append(step.text)
                    row.append(step.comments)

            writer.writerow(row)
