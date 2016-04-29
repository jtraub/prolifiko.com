from django.contrib.auth import authenticate, login as do_login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
import keen

from app.forms import RegistrationForm, LoginForm


def login(request):
    def do_render(f):
        return render(request, 'registration/login.html', {'form': f})

    if request.method is 'GET':
        return do_render(LoginForm())

    form = LoginForm(request.POST)

    if not form.is_valid():
        return do_render(form)

    try:
        u = User.objects.get(email=form.cleaned_data['email'])
    except User.DoesNotExist:
        error = ValidationError('Invalid email address or password',
                                code='bad_email')
        form.add_error(None, error)
        return do_render(form)

    user = authenticate(
        username=u.username,
        password=form.cleaned_data['password']
    )

    if user is None:
        error = ValidationError('Invalid email address or password',
                                code='bad_password')
        form.add_error(None, error)
        return do_render(form)

    do_login(request, user)

    keen.add_event('login', {
        'id': user.id,
        'email': user.email
    })

    return redirect('app_index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            u = form.save()

            user = authenticate(
                username=u.username,
                password=request.POST['password1']
            )

            do_login(request, user)

            keen.add_event('register', {
                'id': user.id,
                'email': user.email
            })

            return redirect('app_index')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
