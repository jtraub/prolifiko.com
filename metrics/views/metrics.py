from datetime import timedelta, datetime, date
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.utils.timezone import make_aware
from django.views.decorators.cache import cache_page
from app.models import Email, Goal, Step
from metrics import data
from app.utils import get_logger


logger = get_logger(__name__)


@staff_member_required
def dashboard(request):
    return render(request, 'dashboard.html')


def funnel(name, users, steps):
    registered = len(users)

    table = [('Registered', registered, '-')]

    for step_name, step_filter in steps:
        logger.info('%s - %s' % (name, step_name))
        users = [u for u in users if step_filter(u)]

        count = len(users)
        rate = "{:3.1f}%".format((count / registered) * 100)
        table.append((step_name, count, rate))

        for user in users:
            logger.debug('- ' + user.email)

    return table


def happy_path(users):
    return funnel('Happy Path', users, [
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


def dr_path(users):
    return funnel('DR', users, [
        ('DR1', lambda u: Email.objects.filter(recipient=u)
         .filter(name='dr1').count() > 0),
        ('DR2', lambda u: Email.objects.filter(recipient=u)
         .filter(name='dr2').count() > 0),
        ('DR3', lambda u: Email.objects.filter(recipient=u)
         .filter(name='dr3').count() > 0),
    ])


def d_path(users):
    return funnel('D', users, [
        ('D1', lambda u: Email.objects.filter(recipient=u)
         .filter(name='d1').count() > 0),
        ('D2', lambda u: Email.objects.filter(recipient=u)
         .filter(name='d2').count() > 0),
        ('D3', lambda u: Email.objects.filter(recipient=u)
         .filter(name='d3').count() > 0),
    ])


@staff_member_required
# @cache_page(60 * 15)
def conversion(request):
    # result = group([happy_path.s(), dr_path.s(), d_path.s()])()
    # .get(timeout=30)

    date_format = '%a %b %d %Y'

    if 'start' in request.GET:
        start = make_aware(datetime.strptime(request.GET['start'],
                                             date_format))
    else:
        start = (timezone.now() - timedelta(days=7)) \
            .replace(hour=0, minute=0, second=0, microsecond=0)

    if 'end' in request.GET:
        end = make_aware(datetime.strptime(request.GET['end'],
                                           date_format))
    else:
        end = timezone.now() \
            .replace(hour=0, minute=0, second=0, microsecond=0)

    # exclude_active = 'exclude_active' in request.GET

    logger.info('Running conversion metric start=%s end=%s' % (start, end))

    users = []
    for user in data.real_users(start, end):
        if start >= user.date_joined or end <= user.date_joined:
            continue

        user.goal = Goal.objects.filter(user=user).first()

        if user.goal and user.goal.deleted:
            continue

        # if exclude_active:
        #     if not user.is_active:
        #         continue
        #
        #     if user.goal and not user.goal.complete:
        #         continue
        #
        #     d_emails = Email.objects \
        #         .filter(recipient=user) \
        #         .filter(name__in=['dr3', 'd3']) \
        #         .count()
        #
        #     if d_emails == 0:
        #         continue

        users.append(user)

    logger.debug('Users:')
    for user in users:
        logger.debug('+ ' + user.email)

    return render(request, 'conversion.html', {
        'happy_path': happy_path(users),
        'dr_path': dr_path(users),
        'd_path': d_path(users),
        'start': start,
        'end': end,
    })
