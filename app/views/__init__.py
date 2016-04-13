from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
import keen

from app.forms import RegistrationForm
from app.models import Goal


@login_required
def index(request):
    user_goals = Goal.objects.filter(user=request.user)
    if len(user_goals) == 0:
        return redirect('app_goals_new')

    goal = user_goals.order_by('-start').first()

    return redirect('app_goals_timeline', goal_id=goal.id)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        u = form.save()

        user = authenticate(
            username=u.username,
            password=request.POST['password1']
        )

        login(request, user)

        keen.add_event('register', {
            'id': user.id,
            'username': user.username,
            'email': user.email
        })

        return redirect('app_index')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
