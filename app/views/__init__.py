from django.contrib.auth.decorators import login_required
from app.models import Goal
from app.subscriptions import is_user_subscribed
from django.shortcuts import redirect, render


@login_required
def index(request):
    active_goals = Goal.objects.filter(user=request.user, complete=False)
    completed_goals = Goal.objects.filter(user=request.user, complete=True)

    if len(active_goals) == 0 and len(completed_goals) == 0:
        return redirect('new_goal')

    return render(request, 'myprogress.html', {
        'active_goals': active_goals,
        'completed_goals': completed_goals,
        'is_subscribed': is_user_subscribed(request.user)
    })


def maintenance(request):
    return render(request, 'maintenance.html')
