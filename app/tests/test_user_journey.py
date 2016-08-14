from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import User
from time import sleep
from unittest.mock import patch, Mock
from unittest import skipIf
from logging import getLogger
from datetime import timedelta
import os

from app.models import Goal, Step

logger = getLogger('prolifiko.app.test_user_journey')


@skipIf('QUICK' in os.environ, reason='Quick run')
class UserJourneyTest(TestCase):
    @override_settings(DEBUG=True,
                       INACTIVE_TIME=24,
                       INACTIVE_TIME_UNIT='seconds',
                       INACTIVE_DELTA=timedelta(seconds=24))
    @patch('django.core.mail.utils.socket')
    def test_user_journey(self, socket):
        socket.getfqdn = Mock(return_value='test')

        from app.tasks import send_d_emails, send_dr_emails
        self.send_dr_emails = send_dr_emails
        self.send_d_emails = send_d_emails

        class Action(object):
            def do(self, user):
                raise RuntimeError('Method not implemented')

        class CreateGoal(Action):
            def do(self, user):
                user.create_goal()

        class CreateStep(Action):
            def do(self, user):
                user.create_step()

                return {
                    1: 'n2_new_goal',
                    2: 'n3_step_1_complete',
                    3: 'n4_step_2_complete',
                    4: 'n5_step_3_complete',
                    5: 'n6_step_4_complete',
                }[user.goal.current_step.number]

        class TrackStep(Action):
            def do(self, user):
                user.track_step()

        class Complete(Action):
            def do(self, user):
                user.complete_goal()

                return 'n7_goal_complete'

        class Email(object):
            def __init__(self, name):
                self.name = name

        spec = {
            'dr': {
                24: [Email('dr1')],
                48: [Email('dr2')],
                72: [Email('dr3')],
            },

            'dr2': {
                0: [CreateGoal()],
                24: [Email('dr1')],
                48: [Email('dr2')],
                72: [Email('dr3')],
            },

            'drd': {
                0: [CreateGoal()],
                24: [Email('dr1')],
                30: [CreateStep()],
                48: [TrackStep(), CreateStep()],
                72: [Email('d1')],
                84: [TrackStep(), CreateStep()],
                108: [Email('d2')],
            },

            'drd2': {
                0: [CreateGoal()],
                24: [Email('dr1')],
                30: [CreateStep()],
                48: [TrackStep(), CreateStep()],
                72: [Email('d1')],
                96: [Email('d2')],
                120: [Email('d3')],
            },

            'h': {
                0: [CreateGoal(), CreateStep()],
                6: [TrackStep(), CreateStep()],
                18: [TrackStep(), CreateStep()],
                30: [TrackStep(), CreateStep()],
                42: [TrackStep(), CreateStep()],
                54: [TrackStep(), Complete()],
            },

            'hd': {
                0: [CreateGoal(), CreateStep()],
                18: [TrackStep(), CreateStep()],
                42: [TrackStep(), CreateStep()],
                66: [Email('d1')],
                90: [Email('d2')],
                114: [Email('d3')],
            },

            'hdh': {
                0: [CreateGoal()],
                12: [CreateStep()],
                30: [TrackStep(), CreateStep()],
                54: [Email('d1')],
                60: [TrackStep(), CreateStep()],
                78: [TrackStep(), CreateStep()],
                102: [Email('d2')],
                108: [TrackStep(), CreateStep()],
            },

            'hdh2': {
                0: [CreateGoal(), CreateStep()],
                18: [TrackStep()],
                42: [Email('d1')],
                48: [CreateStep()],
                66: [TrackStep(), CreateStep()],
                84: [TrackStep(), CreateStep()],
                102: [TrackStep(), CreateStep()],
            }
        }

        time = 0

        users = {name: UserJourneyTest.User.register(name + '@t.com')
                 for name in spec.keys()}

        self.assertInbox([('n1_registration', user.email)
                          for name, user in users.items()])

        while time <= 120:
            print('============ time=%d ============' % time)

            emails = []

            for name, timeline in spec.items():
                if time not in timeline:
                    continue

                user = users[name]

                actions = [event for event in timeline[time]
                           if isinstance(event, Action)]

                for action in actions:
                    email = action.do(user)

                    if email:
                        emails.append((email, user.email))

            self.send_dr_emails()
            self.send_d_emails()

            for name, timeline in spec.items():
                if time not in timeline:
                    continue

                user = users[name]

                emails += [(email.name, user.email) for email in timeline[time]
                           if isinstance(email, Email)]

            self.assertInbox(emails)

            time += 6
            sleep(6)

    def assertInbox(self, emails):
        outbox = [(email.prolifiko_name, email.to[0]) for email in mail.outbox]

        self.assertCountEqual(outbox, emails, {
            'expected': emails,
            'actual': outbox
        })

        mail.outbox = []

    class User:
        def __init__(self, user, client):
            self.user = user
            self.client = client

            self.goal = None

            self.logger = getLogger('prolifiko.app.test_user_journey(%s)' %
                                    self.user.email)

        @staticmethod
        def register(email):
            logger.debug('Registering user %s' % email)

            client = Client()

            client.post(reverse('app_register'), {
                'email': email,
                'password': 'test',
                'first_name': 'test',
            })

            user = User.objects.get(email=email)

            client.login(username=user.username, password='test')

            return UserJourneyTest.User(user, client)

        @property
        def email(self):
            return self.user.email

        def create_goal(self):
            self.logger.debug('Creating goal')

            self.client.post(reverse('app_goals_new'), data={
                'text': 'test goal',
            })

            self.goal = Goal.objects.filter(user=self.user).first()

            return self.goal

        def create_step(self):
            next_step = self.goal.steps.count() + 1
            self.logger.debug('Creating step #%d' % next_step)

            self.client.post(
                reverse('app_steps_new', kwargs={'goal_id': self.goal.id}),
                data={'text': 'test step'},
            )

            self.goal.refresh_from_db()
            return self.goal.steps.last()

        def track_step(self):
            self.logger.debug('Tracking step #%d', self.goal.steps.count())

            step = self.goal.steps.last()

            self.client.post(reverse('app_steps_track', kwargs={
                'goal_id': step.goal.id,
                'step_id': step.id}))

            self.goal.refresh_from_db()

            return self.goal.steps.last()

        def complete_goal(self):
            self.logger.debug('Completing goal')

            self.client.post(reverse('app_goals_complete', kwargs={
                'goal_id': self.goal.id
            }))
