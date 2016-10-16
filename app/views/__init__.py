from django.contrib.auth.decorators import login_required
from app.models import Goal
from django.shortcuts import redirect, render


@login_required
def index(request):
    user_goals = Goal.objects.filter(user=request.user)
    if len(user_goals) == 0:
        return redirect('new_goal')

    return render(request, 'myprogress.html', {
        'goals': user_goals
    })


def maintenance(request):
    return render(request, 'maintenance.html')
