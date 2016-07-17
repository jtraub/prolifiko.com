from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.conf import settings

from app.models import Step, Goal
from app.forms import NewStepForm, TrackStepForm
from app.signals import new_step, step_complete
from app.utils import get_logger, is_active


logger = get_logger(__name__)


@login_required
@is_active
def new(request, goal_id):
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404("Goal does not exist")

    form = NewStepForm()
    status = 200

    if goal.current_step and not goal.current_step.complete:
        return redirect('app_steps_track',
                        goal_id=goal.id, step_id=goal.current_step.id)

    if request.method == 'POST':
        form = NewStepForm(request.POST)

        if form.is_valid():
            step = form.save(commit=False)

            step.goal = goal
            step.start = timezone.now()
            step.end = step.start + settings.INACTIVE_DELTA

            logger.debug('Creating step goal=%s user=%s' % (
                goal.id, request.user.email))

            step.save()

            step.goal.active = True
            step.goal.save()

            goal.refresh_from_db()

            new_step.send('app.views.steps.new', step=step)

            return redirect('app_steps_start',
                            goal_id=goal.id, step_id=step.id)
        else:
            status = 400

    return render(request, 'steps/new.html', {
        'form': form,
        'goal': goal,
        'next_step_num': goal.next_step_num,
        'next_step_nth': goal.next_step_nth
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
@is_active
@load_step
def start(request, step):
    return render(request, 'steps/start.html', {
        'step': step
    })


@login_required
@is_active
@load_step
def track(request, step):
    form = TrackStepForm()

    if request.method == 'POST':
        form = TrackStepForm(request.POST, instance=step)
        step = form.save(commit=False)

        step.time_tracked = timezone.now()
        step.complete = True

        step.save()

        step_complete.send('app.views.steps.track', step=step)

        goal = step.goal
        goal.active = False

        if goal.steps.count() == 5:
            goal.complete = True

        goal.save()

        if goal.complete:
            return redirect('app_goals_complete', goal_id=goal.id)

        return redirect('app_steps_new', goal_id=goal.id)

    return render(request, 'steps/track.html', {
        'step': step,
        'form': form,
    })
