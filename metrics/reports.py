from django.utils.timezone import localtime, is_aware
from app.models import Goal, Email
from metrics.data import five_day_users


def format_date(date):
    return (localtime(date) if is_aware(date) else date) \
        .strftime('%Y-%m-%d %H:%M:%S')


def events(writer):
    writer.writerow([
        'Email', 'Registration', 'N1', 'DR1', 'DR2', 'DR3', 'D1', 'D2', 'D3',
        'Goal', 'Step #1', 'N2', 'Track #1', 'Step #2', 'N3', 'Track #2',
        'Step #3', 'N4', 'Track #3', 'Step #4', 'N5', 'Track #4', 'Step #5',
        'N6', 'Track #5', 'N7'
    ])

    def email_sent(user_emails, email_name):
        for e in user_emails:
            if e.name == email_name:
                return format_date(e.sent)

        return ''

    for user in five_day_users():
        emails = list(Email.objects.filter(recipient=user))

        row = [
            user.email,
            format_date(user.date_joined),
            email_sent(emails, 'n1_registration')
        ]

        email_names = ['DR1', 'DR2', 'DR3', 'D1', 'D2', 'D3']

        for name in email_names:
            email = Email.objects.filter(recipient=user) \
                .filter(name=name.lower()) \
                .first()

            if email:
                row.append(format_date(email.sent))
            else:
                row.append('')

        goal = Goal.objects.filter(user=user).first()

        if goal:
            row.append(format_date(goal.start))

            for step in goal.steps.all():
                row.append(format_date(step.start))

                if step.number == 1:
                    row.append(email_sent(emails, 'n2_new_goal'))
                else:
                    prev_step = step.number - 1
                    row.append(email_sent(emails, 'n%d_step_%d_complete' %
                                          (prev_step + 2, prev_step)))

                if step.complete:
                    row.append(format_date(step.time_tracked))

            row.append(email_sent(emails, 'n7_goal_complete'))

        writer.writerow(row)


def content(writer):
    writer.writerow([
        'Email', 'Goal', 'Step 1', 'Progress 1', 'Step 2', 'Progress 2',
        'Step 3', 'Progress 3', 'Step 4', 'Progress 4', 'Step 5', 'Progress 5',
        'DR1', 'DR2', 'DR3', 'D1', 'D2', 'D3'
    ])

    for user in five_day_users():
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
