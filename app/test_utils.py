from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from unittest.mock import patch, Mock, MagicMock
from django.template.backends.django import Template

from app.models import Goal

from .utils import send_email


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

        send_email('new_goal', user, {'goal': goal})

        socket.getfqdn.assert_any_call()
        loader.get_template.assert_called_once_with('emails/new_goal.html')
        template.render.assert_called_once_with({'user': user, 'goal': goal})

        self.assertEquals(1, len(mail.outbox))
        message = mail.outbox[0]
        self.assertEquals('test', message.subject)
        self.assertEquals(body, message.body)
        self.assertEquals('email@prolifiko.com', message.from_email)
        self.assertEquals([user.email], message.to)
