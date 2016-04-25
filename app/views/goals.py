from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404
import keen

from app.models import Goal
from app.forms import GoalForm


@login_required
def new(request):
    form = GoalForm()
    status = 200

    if request.method == 'POST':
        form = GoalForm(request.POST)

        if form.is_valid():
            goal = form.save(commit=False)

            goal.user = request.user

            goal.save()

            keen.add_event('goals.new', {
                'id': goal.id.hex,
                'user_id': goal.user.id
            })

            return redirect('app_steps_new', goal_id=goal.id)
        else:
            status = 400

    return render(request, 'goals/new.html', {
        'form': form,
    }, status=status)


@login_required
def timeline(request, goal_id):
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404('Goal does not exist')

    if goal.steps.count() == 0:
        return redirect('app_steps_new', goal_id=goal.id)

    return render(request, 'goals/timeline.html', {
        'goal': goal
    })
