from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
import keen

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

        keen.add_event('register', {
            'id': user.id,
            'username': user.username,
            'email': user.email
        })

        return redirect('app_index')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
