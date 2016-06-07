from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.core import mail
from unittest.mock import patch, Mock
from django.template.backends.django import Template
from django.conf import settings
from html2text import html2text
from requests.models import Response

from app.models import Goal, Email

from app import utils


class UtilsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@real.com')

    @patch('app.utils.loader')
    @patch('django.core.mail.utils.socket')
    @override_settings(EMAIL_META={'test': {'subject': 'Test Subject'}})
    def test_send_email(self, socket, loader):
        socket.getfqdn = Mock(return_value='test')

        goal = Mock(spec=Goal)

        body = 'some email body'

        template = Mock(spec=Template)
        template.render.return_value = body
        loader.get_template = Mock(return_value=template)

        utils.send_email('test', self.user, {'goal': goal})

        loader.get_template.assert_called_once_with('emails/test.html')
        template.render.assert_called_once_with({
            'user': self.user,
            'goal': goal,
            'BASE_URL': settings.BASE_URL
        })

        self.assertEquals(1, len(mail.outbox))
        message = mail.outbox[0]

        self.assertEquals('Test Subject', message.subject)
        self.assertEquals('Bec and Chris', message.from_email)
        self.assertEquals([self.user.email], message.to)

        self.assertEquals(html2text(body), message.body)
        self.assertEquals((body, 'text/html'), message.alternatives[0])

        self.assertEquals('test', message.prolifiko_name)

        emails = Email.objects.filter(recipient=self.user)
        self.assertEquals(1, emails.count())
        email = emails.first()
        self.assertEquals('test', email.name)

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
