from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.core import mail
from unittest.mock import patch, Mock, MagicMock
from django.template.backends.django import Template
from html2text import html2text

from app.models import Goal

from . import utils


class UtilsTest(TestCase):
    fixtures = ['users', 'goals', 'steps']

    @patch('app.utils.loader')
    @patch('django.core.mail.utils.socket')
    def test_send_email(self, socket, loader):
        socket.getfqdn = Mock(return_value='test')

        user = User.objects.get(username='test')
        goal = Goal.objects.all().first()

        body = 'some email body;'

        template = Mock(spec=Template)
        template.render.return_value = body
        loader.get_template = Mock(return_value=template)

        utils.send_email('new_goal', user, {'goal': goal})

        socket.getfqdn.assert_any_call()
        loader.get_template.assert_called_once_with('emails/new_goal.html')
        template.render.assert_called_once_with({'user': user, 'goal': goal})

        self.assertEquals(1, len(mail.outbox))
        message = mail.outbox[0]

        self.assertEquals('test', message.subject)
        self.assertEquals('email@prolifiko.com', message.from_email)
        self.assertEquals([user.email], message.to)

        self.assertEquals(html2text(body), message.body)
        self.assertEquals((body, 'text/html'), message.alternatives[0])

    @override_settings(DEBUG=True)
    def test_add_event_debug(self):
        collection = 'test'
        body = {'foo': 'bar'}

        utils.add_event(collection, body)

        self.assertEquals(1, len(utils.events))
        self.assertEquals({'collection', collection, 'body', body},
                          utils.events[0])

    @override_settings(DEBUG=False)
    @patch('app.utils.keen')
    def test_add_event_debug(self, keen):
        collection = 'test'
        body = {'foo': 'bar'}

        utils.add_event(collection, body)

        keen.add_event.assert_called_with(collection, body)
