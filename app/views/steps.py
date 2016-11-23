from datetime import datetime, time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.utils import timezone
import pytz

from app.models import Step, Goal, Timezone
from app.forms import NewStepForm, TrackStepForm
from app.signals import new_step, step_complete, goal_complete
from app.utils import get_logger, is_active, parse_date

logger = get_logger(__name__)


def create_midnight_step(params, goal, step_start, tz):
    valid = 'step_name' in params and 'step_description' in params

    if not valid:
        raise ValueError('Invalid midnight step params %s' % params)

    logger.debug('Creating midnight step goal=%s user=%s' % (
        goal.id, goal.user.email))

    return goal.create_step(params['step_name'],
                            params['step_description'],
                            step_start,
                            Step.midnight_deadline(step_start, tz),
                            commit=True)


def create_step(params, goal, step_start, tz):
    valid = 'step_name' in params \
            and 'step_deadline' in params

    if not valid:
        raise ValueError('Invalid custom step params %s' % params)

    logger.debug('Creating step goal=%s user=%s' % (
        goal.id, goal.user.email))

    deadline_date = parse_date(params['step_deadline'])
    deadline_midnight = datetime.combine(deadline_date, time())
    deadline_utc = tz \
        .localize(deadline_midnight) \
        .astimezone(pytz.utc)

    description = params['step_description'] \
        if 'step_description' in params else None

    return goal.create_step(params['step_name'],
                            description,
                            step_start,
                            deadline_utc,
                            commit=True)


@login_required
@is_active
def new(request, goal_id):
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404("Goal does not exist")

    if goal.current_step and not goal.current_step.complete:
        return redirect('complete_step',
                        goal_id=goal.id, step_id=goal.current_step.id)

    if request.method == 'POST':
        tz = pytz.timezone(Timezone.objects.get(user=request.user).name)
        step_start = timezone.now()

        try:
            if goal.is_five_day:
                step = create_midnight_step(request.POST, goal, step_start, tz)
            else:
                step = create_step(request.POST, goal, step_start, tz)

            new_step.send('app.views.steps.new', step=step)

            if goal.is_five_day:
                return redirect('start_step', goal_id=goal.id, step_id=step.id)

            return redirect('myprogress')
        except ValueError:
            logger.exception('Failed to create step')
            return HttpResponseBadRequest()

    return render(request, 'steps/new.html', {
        'next_step_num': goal.next_step_num,
        'data': {
            'stepNumber': goal.next_step_num,
            'goalId': goal.id.hex,
        }
    })


def latest(request, goal_id):
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404("Goal does not exist")

    if goal.steps.count() == 0:
        return redirect('new_step', goal_id=goal.id)

    latest_step = goal.steps.last()

    return redirect('complete_step',
                    goal_id=goal_id, step_id=latest_step.id)


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
    return render(request, 'steps/start_five_day.html', {
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

        if goal.type == Goal.TYPE_FIVE_DAY:
            if goal.steps.count() == 5:
                goal.complete = True

                for step in [s for s in goal.steps.all() if not s.complete]:
                    step.complete = True
                    step.save()

                goal_complete.send('app.views.steps.track', goal=goal)

            goal.save()

            # five day challenges should be shown the feedback page when
            # they've finished
            if goal.complete:
                return redirect('feedback')

            # five day challenges should be forced to create a new step
            return redirect('new_step', goal_id=goal.id)

        # non five day challenges go to dashboard where users can complete
        # goals or start a new step
        return redirect('myprogress')

    template = 'steps/track_five_day.html' \
        if step.goal.type == Goal.TYPE_FIVE_DAY \
        else 'steps/track.html'

    return render(request, template, {
        'step': step,
        'form': form,
    })
