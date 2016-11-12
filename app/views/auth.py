from django.contrib.auth import authenticate, login as do_login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from app.forms import RegistrationForm, LoginForm
from app.utils import add_event, get_logger
from app.signals import registration
from app.subscriptions import is_user_subscribed

logger = get_logger(__name__)


def login(request):
    def do_render(f):
        return render(request, 'registration/login.html', {'form': f})

    def do_error(code):
        error = ValidationError('Invalid email address or password',
                                code=code)

        form.add_error(None, error)
        return do_render(form)

    if request.method == 'GET':
        return do_render(LoginForm())

    form = LoginForm(request.POST)

    if not form.is_valid():
        return do_render(form)

    try:
        u = User.objects.get(email=form.cleaned_data['email'])
    except User.DoesNotExist:
        return do_error('bad_email')

    user = authenticate(
        username=u.username,
        password=form.cleaned_data['password']
    )

    if user is None:
        return do_error('bad_password')

    if not user.is_active:
        return redirect('deactivate', user_id=user.id)

    do_login(request, user)

    add_event('login', user)

    return redirect('myprogress')


def register(request):
    status = 200

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            logger.debug('Registering user email=%s' %
                         form.cleaned_data['email'])
            user = form.save()

            registration.send('app.views.auth.register', user=user)

            if is_user_subscribed(user):
                # Log registered users in so that they can go straight from
                # the welcome page to creating a goal. Five day challenge users
                # need to check their inbox first.
                authenticated_user = authenticate(
                    username=user.username,
                    password=form.cleaned_data['password'])

                do_login(request, authenticated_user)

            return redirect('welcome')
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            logger.debug('Registration failed ' + str(errors))
            status = 400

    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form},
                  status=status)


def welcome(request):
    if request.user.is_authenticated() and is_user_subscribed(request.user):
        return render(request, 'registration/continue_registered.html')
    else:
        return render(request, 'registration/check_inbox.html')
