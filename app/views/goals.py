from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseBadRequest, HttpResponseNotAllowed
from django.db import transaction
from django.utils import timezone
import pytz

from app.models import Goal, Step
from app.signals import new_goal, goal_complete, new_step
from app.utils import get_logger, is_active

logger = get_logger(__name__)


@login_required
@is_active
def new(request):
    current_goal = Goal.objects.filter(user=request.user).first()

    if current_goal:
        return redirect('app_goals_timeline', goal_id=current_goal.id)

    if request.method == 'GET':
        return render(request, 'goals/new.html', {
            'timezones': pytz.common_timezones
        })

    if request.method != 'POST':
        return HttpResponseNotAllowed(['GET', 'POST'])

    is_valid = 'text' in request.POST and \
               'first_step' in request.POST and \
               'timezone' in request.POST

    if not is_valid:
        return HttpResponseBadRequest()

    start = timezone.now()

    goal = Goal(
        user=request.user,
        timezone=request.POST['timezone'],
        text=request.POST['text'],
        start=start
    )

    with transaction.atomic():
        logger.info('Creating goal user=%s' % goal.user.email)

        goal.save()

        logger.info('Creating first step goal=%s user=%s' % (
            goal.id, request.user.email))

        first_step = goal.create_step(request.POST['first_step'],
                                      goal.start,
                                      commit=True)

    new_goal.send('app.views.goals.new', goal=goal)
    new_step.send('app.views.goals.new', step=first_step)

    return redirect('app_steps_start', goal_id=goal.id, step_id=first_step.id)


@login_required
@is_active
def timeline(request, goal_id):
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404('Goal does not exist')

    if goal.steps.count() == 0:
        return redirect('app_steps_new', goal_id=goal.id)

    in_progress = goal.steps.filter(complete=False).count() > 0

    return render(request, 'goals/timeline.html', {
        'goal': goal,
        'in_progress': in_progress
    })


@login_required
@is_active
def complete(request, goal_id):
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404('Goal does not exist')

    if request.method == 'POST':
        logger.info('Goal complete user=%s' % goal.user.email)

        goal.complete = True
        goal.save()

        goal_complete.send('app.views.goals.complete', goal=goal)

        return render(request, 'goals/feedback.html', {'goal': goal})

    return render(request, 'goals/complete.html', {'goal': goal})
