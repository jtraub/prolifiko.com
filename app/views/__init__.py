from django.contrib.auth.decorators import login_required
from app.models import Goal
from django.shortcuts import redirect


@login_required
def index(request):
    user_goals = Goal.objects.filter(user=request.user)
    if len(user_goals) == 0:
        return redirect('new_goal')

    goal = user_goals.order_by('-start').first()

    return redirect('app_goals_timeline', goal_id=goal.id)
