import json
from datetime import timedelta, time, datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseBadRequest, HttpResponseNotAllowed
from django.db import transaction
from django.utils import timezone
import pytz

from app.models import Goal, Step, Timezone
from app.signals import new_goal, goal_complete, new_step
from app.utils import get_logger, is_active, parse_date
from app.subscriptions import is_user_subscribed

logger = get_logger(__name__)


def new_five_day_challenge(user, params, start, timezone):
    is_valid = 'goal_name' in params and \
               'goal_description' in params and \
               'step_name' in params and \
               'step_description' in params

    if not is_valid:
        raise ValueError('Invalid request params %s' % params)

    goal = Goal(
        user=user,
        type=Goal.TYPE_FIVE_DAY,
        name=params['goal_name'],
        description=params['goal_description'],
        start=start,
        target=(start + timedelta(days=5)).date(),
    )

    with transaction.atomic():
        logger.info('Creating 5 day challenge user=%s' % goal.user.email)

        goal.save()

        logger.info('Creating 5 day challenge first step goal=%s user=%s' % (
            goal.id, user.email))

        goal.create_step(params['step_name'],
                         params['step_description'],
                         start,
                         Step.midnight_deadline(start, timezone),
                         commit=True)

    return goal


def new_custom_goal(user, params, start, timezone):
    is_valid = 'goal_name' in params and \
               'goal_target' in params and \
               'step_name' in params and \
               'step_deadline' in params

    if not is_valid:
        raise ValueError('Invalid request params %s' % params)

    goal = Goal(
        user=user,
        type=Goal.TYPE_CUSTOM,
        name=params['goal_name'],
        start=start,
        target=parse_date(params['goal_target']),
    )

    if 'goal_description' in params:
        goal.description = params['goal_description']

    with transaction.atomic():
        logger.info('Creating custom goal user=%s' % goal.user.email)

        goal.save()

        logger.info('Creating custom goal first step goal=%s user=%s' % (
            goal.id, user.email))

        deadline_date = parse_date(params['step_deadline'])
        deadline_midnight = datetime.combine(deadline_date, time())
        deadline_utc = timezone \
            .localize(deadline_midnight) \
            .astimezone(pytz.utc)

        step_description = params['step_description'] \
            if 'step_description' in params else None

        goal.create_step(params['step_name'],
                         step_description,
                         start,
                         deadline_utc,
                         commit=True)

    return goal


@login_required
@is_active
def new(request):
    if 'subscribed' in request.GET:
        user_is_subscribed = request.GET['subscribed'] == 'true'
    else:
        user_is_subscribed = is_user_subscribed(request.user)

    if not user_is_subscribed:
        current_goal = Goal.objects \
            .filter(user=request.user, type=Goal.TYPE_FIVE_DAY) \
            .first()

        if current_goal:
            logger.debug('Redirecting free user to existing goal user=%s' %
                         current_goal.user.email)
            return redirect('myprogress')

    if request.method == 'GET':
        logger.debug('Rendering new goal form is_subscribed=%s' %
                     user_is_subscribed)
        is_first_goal = Goal.objects.filter(user=request.user).count() == 0
        return render(request, 'goals/new.html', {
            'user_is_subscribed': user_is_subscribed,
            'data': json.dumps({
                'isFirstGoal': is_first_goal
            })
        })

    if request.method != 'POST':
        return HttpResponseNotAllowed(['GET', 'POST'])

    if 'type' not in request.POST:
        logger.warn('"type" not found in new goal request')
        return HttpResponseBadRequest()

    tz = pytz.timezone(Timezone.objects.get(user=request.user).name)

    start = timezone.now()

    try:
        if request.POST['type'] == Goal.TYPE_FIVE_DAY:
            goal = new_five_day_challenge(request.user,
                                          request.POST,
                                          start,
                                          tz)
        else:
            goal = new_custom_goal(request.user,
                                   request.POST,
                                   start,
                                   tz)
    except ValueError:
        logger.exception('Failed to create goal')
        return HttpResponseBadRequest()

    first_step = goal.steps.first()

    new_goal.send('app.views.goals.new', goal=goal)
    new_step.send('app.views.goals.new', step=first_step)

    if goal.type == Goal.TYPE_FIVE_DAY:
        return redirect('start_step', goal_id=goal.id, step_id=first_step.id)
    else:
        return redirect('start_goal', goal_id=goal.id)


@login_required
@is_active
def timeline(request, goal_id):
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404('Goal does not exist')

    if goal.steps.count() == 0:
        return redirect('new_step', goal_id=goal.id)

    in_progress = goal.steps.filter(complete=False).count() > 0

    return render(request, 'goals/timeline.html', {
        'goal': goal,
        'in_progress': in_progress
    })


@login_required
@is_active
def complete(request, goal_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['GET'])

    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404('Goal does not exist')

    logger.info('Goal complete user=%s' % goal.user.email)

    goal.complete = True

    for step in goal.steps.all():
        if not step.complete:
            step.complete = True
            step.save()

    goal.save()

    goal_complete.send('app.views.goals.complete', goal=goal)

    return render(request, 'goals/complete.html', {'goal': goal})


@login_required
@is_active
def start(request, goal_id):
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404('Goal does not exist')

    return render(request, 'goals/start.html', {'goal': goal})
