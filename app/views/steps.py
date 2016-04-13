from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404

from app.models import Step, Goal
from app.forms import StepForm


@login_required
def new(request, goal_id):
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404("Goal does not exist")

    form = StepForm()
    status = 200

    if request.method == 'POST':
        form = StepForm(request.POST)

        if form.is_valid():
            step = form.save(commit=False)
            step.user = request.user
            goal.save()

            return redirect('app_steps_new', goal=goal.id)
        else:
            status = 400

    return render(request, 'goals/new.html', {
        'form': form,
        'first': Step.objects.filter(user=request.user).count() == 0
    }, status=status)
