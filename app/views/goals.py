from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta

from app.models import Goal
from app.forms import GoalForm
from app.signals import new_goal, goal_complete
from app.utils import get_logger, is_active

logger = get_logger(__name__)


@login_required
@is_active
def new(request):
    form = GoalForm()
    status = 200

    if request.method == 'POST':
        form = GoalForm(request.POST)

        if form.is_valid():
            goal = form.save(commit=False)

            goal.user = request.user

            days_since_start = relativedelta(now(), goal.user.date_joined).days
            goal.lives = 3 - days_since_start

            logger.debug('Creating goal user=%s' % goal.user.email)

            goal.save()

            new_goal.send('app.views.goals.new', goal=goal)

            return redirect('app_steps_new', goal_id=goal.id)
        else:
            status = 400

    return render(request, 'goals/new.html', {
        'form': form,
    }, status=status)


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
