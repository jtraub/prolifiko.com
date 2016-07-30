from django.utils.timezone import localtime
from app.models import Goal, Email
from metrics.data import real_users


def format_date(date):
    return localtime(date).strftime('%Y-%m-%d %H:%M:%S')


def events(writer):
    writer.writerow([
        'Email', 'Registration', 'New Goal', 'Step #1', 'Track #1',
        'Step #2', 'Track #2', 'Step #3', 'Track #3', 'Step #4',
        'Track #4', 'Step #5', 'Track #5'
    ])

    for user in real_users():
        row = [
            user.email,
            format_date(user.date_joined)
        ]

        goal = Goal.objects.filter(user=user).first()

        if goal:
            row.append(format_date(goal.start))

            for step in goal.steps.all():
                row.append(format_date(step.start))
                row.append(format_date(step.time_tracked))

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
                row.append(format_date(email.sent))
            else:
                row.append('')

        writer.writerow(row)
