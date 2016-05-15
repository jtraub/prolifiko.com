from django.contrib.auth.models import User
from django.template import loader
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from typing import Dict
import keen
import logging
from html2text import html2text

events = []


def get_logger(name: str):
    return logging.getLogger('prolifiko.%s' % name)

logger = get_logger(__name__)


def send_email(name: str, user: User, context: Dict):
    template = loader.get_template('emails/%s.html' % name)

    context.setdefault('user', user)

    html = template.render(context)
    text = html2text(html)

    logger.info('Sending %s email to %s' % (name, user.email))

    msg = EmailMultiAlternatives(
        'test', text, 'email@prolifiko.com', [user.email])
    msg.attach_alternative(html, 'text/html')
    msg.send()


def add_event(collection, body):
    if settings.DEBUG:
        events.append({'collection': collection, 'body': body})
    else:
        keen.add_event(collection, body)
