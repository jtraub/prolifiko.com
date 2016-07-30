import sys
import csv
from app.models import Goal, Email
from metrics.data import real_users


def events(writer):
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


def content(writer):
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


def emails(writer):
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
