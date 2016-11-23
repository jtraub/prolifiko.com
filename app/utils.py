from datetime import datetime
from django.contrib.auth.models import User
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import redirect
import keen
import logging
from html2text import html2text
from typing import Dict

from .models import Email, Goal
from .signals import email as email_signal

events = []


def get_logger(name: str):
    return logging.getLogger('prolifiko.%s' % name)


logger = get_logger(__name__)


def render_email(name: str, user: User, goal: Goal=None, extra=None):
    template = loader.get_template('emails/%s.html' % name)

    context = {
        'user': user,
        'BASE_URL': settings.BASE_URL
    }

    if goal:
        context['goal'] = goal

    if extra:
        context = {**context, **extra}

    try:
        html = template.render(context)
    except Exception as e:
        logger.error('%s raised when rendering %s email; %s' %
                     (type(e).__name__, name, e))

        raise e

    text = html2text(html)

    return html, text


def send_email(name: str, user: User, goal: Goal=None, context=None):
    if not user.is_active:
        raise ValueError('Cannot send email to inactive user ' + user.email)

    (html, text) = render_email(name, user, goal, context)

    meta = settings.EMAIL_META[name]

    logger.info('Sending %s email user=%s' % (name, user.email))

    if user.email[-8:] == 'test.com':
        recipient = 'prolifikotest@gmail.com'
    else:
        recipient = user.email

    msg = EmailMultiAlternatives(
        meta['subject'],
        text,
        settings.DEFAULT_FROM_EMAIL,
        [recipient]
    )
    msg.prolifiko_name = name
    msg.attach_alternative(html, 'text/html')

    msg.send()

    result = Email.objects.create(name=name, recipient=user)

    email_signal.send('app.utils.send_email', email=result)

    return result


def is_real_user(user: User):
    if user.is_staff:
        return False

    if user.email in settings.TEST_EMAIL_ADDRESSES:
        return False

    for domain in settings.TEST_EMAIL_DOMAINS:
        if user.email.endswith(domain):
            return False

    return True


def add_event(collection, user: User, body: Dict=None):
    if not is_real_user(user):
        logger.info('Skipping keen event user=%s' % user.email)
        return

    if body is None:
        body = {}

    body['user_id'] = user.id
    body['email'] = user.email

    logger.info('Recording %s event %s user=%s' %
                (collection, str(body), user.email))

    if settings.DEBUG:
        events.append({'collection': collection, 'body': body})
    else:
        keen.add_event(collection, body)


def is_active(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_active:
            return redirect('deactivate', user_id=request.user.id)

        return view_func(request, *args, **kwargs)

    return wrapper


def parse_date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()
