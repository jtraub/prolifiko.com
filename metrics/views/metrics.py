import datetime
from celery import group, shared_task
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import os
from django.views.decorators.cache import cache_page
from app.models import Email, Goal, Step
from metrics import data
from app.utils import get_logger


logger = get_logger(__name__)


@staff_member_required
def dashboard(request):
    return render(request, 'dashboard.html')


def funnel(name, steps):
    users = []
    for user in data.real_users():
        user.goal = Goal.objects.filter(user=user).first()

        if user.goal and user.goal.deleted:
            continue

        users.append(user)

    registered = len(users)

    for user in users:
        user.goal = Goal.objects.filter(user=user).first()

    table = [('Registered', registered, '-')]

    for step_name, step_filter in steps:
        logger.info('%s - %s' % (name, step_name))
        users = [u for u in users if step_filter(u)]

        count = len(users)
        rate = "{:3.1f}%".format((count / registered) * 100)
        table.append((step_name, count, rate))

    return table


@shared_task
def happy_path():
    return funnel('Happy Path', [
        ('New Goal', lambda u: u.goal),
        ('Step #1', lambda u: Step.objects.filter(goal=u.goal).count() > 0),
        ('Track #1', lambda u: Step.objects.filter(goal=u.goal)[0].complete),
        ('Step #2', lambda u: Step.objects.filter(goal=u.goal).count() > 1),
        ('Track #2', lambda u: Step.objects.filter(goal=u.goal)[1].complete),
        ('Step #3', lambda u: Step.objects.filter(goal=u.goal).count() > 2),
        ('Track #3', lambda u: Step.objects.filter(goal=u.goal)[2].complete),
        ('Step #4', lambda u: Step.objects.filter(goal=u.goal).count() > 4),
        ('Track #4', lambda u: Step.objects.filter(goal=u.goal)[3].complete),
        ('Step #5', lambda u: Step.objects.filter(goal=u.goal).count() > 4),
        ('Track #5', lambda u: Step.objects.filter(goal=u.goal)[4].complete),
        ('Complete', lambda u: u.goal.complete)
    ])


@shared_task
def dr_path():
    return funnel('DR', [
        ('DR1', lambda u: Email.objects.filter(recipient=u)
         .filter(name='dr1').count() > 0),
        ('DR2', lambda u: Email.objects.filter(recipient=u)
         .filter(name='dr2').count() > 0),
        ('DR3', lambda u: Email.objects.filter(recipient=u)
         .filter(name='dr3').count() > 0),
    ])


@shared_task
def d_path():
    return funnel('D', [
        ('D1', lambda u: Email.objects.filter(recipient=u)
         .filter(name='d1').count() > 0),
        ('D2', lambda u: Email.objects.filter(recipient=u)
         .filter(name='d2').count() > 0),
        ('D3', lambda u: Email.objects.filter(recipient=u)
         .filter(name='d3').count() > 0),
    ])


@staff_member_required
@cache_page(60 * 15)
def conversion(request):
    # result = group([happy_path.s(), dr_path.s(), d_path.s()])()
    # .get(timeout=30)

    return render(request, 'conversion.html', {
        'happy_path': happy_path(),
        'dr_path': dr_path(),
        'd_path': d_path(),
    })
