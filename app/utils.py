from django.contrib.auth.models import User
from django.template import loader
from django.core.mail import send_mail
from typing import Dict

import logging


def get_logger(name):
    return logging.getLogger('prolifiko.%s' % name)

logger = get_logger(__name__)


def send_email(name: str, user: User, context: Dict):
    template = loader.get_template('emails/%s.html' % name)

    context.setdefault('user', user)

    body = template.render(context)

    logger.info('Sending %s email to %s' % (name, user.email))

    send_mail('test', body, 'email@prolifiko.com', [user.email])
