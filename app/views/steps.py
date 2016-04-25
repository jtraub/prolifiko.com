from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.utils import timezone
from datetime import timedelta
import keen

from app.models import Step, Goal
from app.forms import NewStepForm, TrackStepForm


@login_required
def new(request, goal_id):
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404("Goal does not exist")

    form = NewStepForm()
    status = 200

    if request.method == 'POST':
        form = NewStepForm(request.POST)

        if form.is_valid():
            step = form.save(commit=False)

            step.goal = goal
            step.start = timezone.now()
            step.end = step.start + timedelta(days=1)

            step.save()

            keen.add_event('steps.new', {
                'id': step.id,
                'user_id': request.user.id,
                'goal_id': step.goal.id
            })

            return redirect('app_steps_start',
                            goal_id=goal.id, step_id=step.id)
        else:
            status = 400

    return render(request, 'steps/new.html', {
        'form': form,
        'first': Step.objects.filter(goal=goal).count() == 0,
        'goal': goal
    }, status=status)


def load_step(view):
    def wrapper(request, goal_id, step_id):
        try:
            step = Step.objects.get(pk=step_id, goal_id=goal_id)
        except Step.DoesNotExist:
            raise Http404("Step does not exist")

        if step.goal.user.id is not request.user.id:
            return HttpResponse('Unauthorized', status=401)

        return view(request, step)

    return wrapper


@login_required
@load_step
def start(request, step):
    return render(request, 'steps/start.html', {
        'step': step
    })


@login_required
@load_step
def track(request, step):
    form = TrackStepForm()

    if request.method == 'POST':
        form = TrackStepForm(request.POST, instance=step)
        step = form.save(commit=False)

        step.complete = True

        step.save()

        keen.add_event('steps.track', {
            'id': step.id,
            'user_id': request.user.id,
            'goal_id': step.goal.id
        })

        return redirect('app_steps_complete',
                        goal_id=step.goal.id, step_id=step.id)

    return render(request, 'steps/track.html', {
        'step': step,
        'form': form
    })


@login_required
@load_step
def complete(request, step):
    return render(request, 'steps/complete.html', {
        'step': step
    })


# This only used for completing a step atm.
@login_required
@load_step
def update(request, step):
    if request.method == 'POST':
        step.complete = True

        keen.add_event('steps.complete', {
            'id': step.id,
            'user_id': request.user.id,
            'goal_id': step.goal.id
        })

        step.save()

    return redirect('app_goals_timeline', goal_id=step.goal.id)

