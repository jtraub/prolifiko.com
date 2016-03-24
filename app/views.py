from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import *


@login_required
def index(request):
    return render(request, 'index.html', {
        'user': request.user
    })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        u = form.save()

        user = authenticate(
            username=u.username,
            password=request.POST['password1']
        )

        login(request, user)

        return redirect('app_index')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
