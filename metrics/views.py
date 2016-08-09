from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import os
from app.models import Goal, Email
from metrics import data, reports
import csv
from django.utils.timezone import localtime


@staff_member_required
def user_journey(request):
    return render(request, 'user_journey.html', {
        'project_id': os.environ['KEEN_PROJECT_ID'],
        'read_key': os.environ['KEEN_READ_KEY'],
        'real_users': [user.email for user in data.real_users()],
    })


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


@staff_member_required
def list_reports(request):
    return render(request, 'reports.html')


@staff_member_required
def csv_report(request, name):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % name

    getattr(reports, name)(csv.writer(response))

    return response
