from django.contrib.auth.models import User
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from typing import Dict
import keen
import logging
from html2text import html2text

events = []
nth = {
    1: 'first',
    2: 'second',
    3: 'third',
    4: 'fourth',
    5: 'fifth',
}


def get_logger(name: str):
    return logging.getLogger('prolifiko.%s' % name)


logger = get_logger(__name__)


def render_email(name: str, user: User, context: Dict):
    template = loader.get_template('emails/%s.html' % name)

    context.setdefault('user', user)
    context['BASE_URL'] = settings.BASE_URL

    try:
        html = template.render(context)
    except Exception as e:
        logger.error('%s raised when rendering %s email; %s' %
                     (e.__name__, name, e))

        raise e

    text = html2text(html)

    return html, text


def send_email(name: str, user: User, context: Dict={}):
    (html, text) = render_email(name, user, context)

    meta = settings.EMAIL_META[name]

    logger.debug('Sending %s email to %s' % (name, user.email))

    if user.email[-8:] == 'test.com':
        recipient = 'prolifikotest@gmail.com'
    else:
        recipient = user.email

    msg = EmailMultiAlternatives(
        meta['subject'], text, 'email@prolifiko.com', [recipient])
    msg.attach_alternative(html, 'text/html')
    msg.send()


def add_event(collection, body):
    if settings.DEBUG:
        events.append({'collection': collection, 'body': body})
    else:
        logger.debug('Recording %s event %s' % (collection, str(body)))
        keen.add_event(collection, body)
