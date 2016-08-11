from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from app.models import Goal, Email
from metrics import data
from django.utils.timezone import localtime


@staff_member_required
def active_users(request):
    return render(request, 'active_users.html', {
        'active_users': data.active_users()
    })


@staff_member_required
def user_history(request):
    if 'email' not in request.GET:
        return render(request, 'user_history.html')

    email = request.GET['email']

    history = []

    user = User.objects.get(email=email)

    history.append(('Registered', user.date_joined))

    goal = Goal.objects.filter(user=user).first()

    for email in Email.objects.filter(recipient=user):
        if goal and email.step and email.step.goal.id != goal.id:
            continue

        history.append(('Sent %s email' % email.name, email.sent))

    if goal:
        history.append(('Goal started', goal.start))

        for step in goal.steps.all():
            start_time = localtime(step.end).strftime('%a %d %H:%M')
            started_label = 'Step #%d started (due %s) (%s)' % (
                step.number, start_time, step.id)
            history.append((started_label, step.start))

            if step.complete:
                history.append(('Step #%d tracked' % step.number,
                                step.time_tracked))

    history.sort(key=lambda e: e[1])

    return render(request, 'user_history.html', {
        'history': history,
        'goal': goal,
        'user': user
    })
