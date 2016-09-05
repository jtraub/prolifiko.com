from django.contrib.auth.models import User
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import redirect
import keen
import logging
from html2text import html2text
from django_mailgun import MailgunAPIError
from typing import Dict

from .models import Email, Goal

events = []


def get_logger(name: str):
    return logging.getLogger('prolifiko.%s' % name)


logger = get_logger(__name__)


def render_email(name: str, user: User, goal: Goal=None):
    template = loader.get_template('emails/%s.html' % name)

    context = {
        'user': user,
        'BASE_URL': settings.BASE_URL
    }

    if goal:
        context['goal'] = goal

    try:
        html = template.render(context)
    except Exception as e:
        logger.error('%s raised when rendering %s email; %s' %
                     (type(e).__name__, name, e))

        raise e

    text = html2text(html)

    return html, text


def send_email(name: str, user: User, goal: Goal=None):
    if not user.is_active:
        raise ValueError('Cannot send email to inactive user ' + user.email)

    (html, text) = render_email(name, user, goal)

    meta = settings.EMAIL_META[name]

    logger.debug('Sending %s email to %s' % (name, user.email))

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

    try:
        msg.send()
    except MailgunAPIError as e:
        response = e.args[0]

        msg = 'MailgunAPIError sending %s email to %s ' + \
              'status_code=%d content=%s'

        raise MailgunAPIError(msg % (
                name, user.email, response.status_code, response.text))

    return Email.objects.create(name=name, recipient=user)


def add_event(collection, user: User, body: Dict=None):
    if user.is_staff:
        logger.debug('Skipping staff user event')
        return

    if user.email in settings.TEST_EMAIL_ADDRESSES:
        logger.debug('Skipping test user event')
        return

    for domain in settings.TEST_EMAIL_DOMAINS:
        if user.email.endswith(domain):
            logger.debug('Skipping test user event')
            return

    if body is None:
        body = {}

    body['user_id'] = user.id
    body['email'] = user.email

    if settings.DEBUG:
        events.append({'collection': collection, 'body': body})
    else:
        logger.debug('Recording %s event %s' % (collection, str(body)))
        keen.add_event(collection, body)


def is_active(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_active:
            return redirect('app_deactivate', user_id=request.user.id)

        return view_func(request, *args, **kwargs)

    return wrapper
