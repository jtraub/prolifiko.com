from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.utils import timezone
from datetime import timedelta

from app.models import Step, Goal
from app.forms import NewStepForm, TrackStepForm
from app.signals import new_step, step_complete
from app.utils import get_logger


logger = get_logger(__name__)


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

            logger.debug('Creating step goal=%s user=%s' % (
                goal.id, request.user.email))

            step.save()

            goal.refresh_from_db()

            new_step.send('app.views.steps.new', step=step)

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

        step_complete.send('app.views.steps.track', step=step)

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
