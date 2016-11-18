from django.contrib.auth.decorators import login_required
from app.models import Goal
from app.subscriptions import is_user_subscribed
from django.shortcuts import redirect, render


@login_required
def index(request):
    active_goal = Goal.objects \
        .filter(user=request.user, complete=False) \
        .first()
    completed_goals = Goal.objects.filter(user=request.user, complete=True)

    if not active_goal and len(completed_goals) == 0:
        return redirect('new_goal')

    return render(request, 'myprogress.html', {
        'active_goal': active_goal,
        'completed_goals': completed_goals,
        'user_is_subscribed': is_user_subscribed(request.user)
    })


def maintenance(request):
    return render(request, 'maintenance.html')


def feedback(request):
    if not is_user_subscribed(request.user):
        return render(request, 'feedback_five_day.html')
