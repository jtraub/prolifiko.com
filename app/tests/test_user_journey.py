from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import User
from time import sleep
from unittest.mock import patch, Mock
from unittest import skip
from logging import getLogger
from datetime import timedelta

from app.models import Goal, Step

logger = getLogger('prolifiko.app.test_user_journey')


@skip
# @skipIf('QUICK' in os.environ, reason='Quick run')
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
            def __init__(self, name, lives=3):
                self.name = name
                self.lives = lives

        spec = {
            'dr': (0, {
                '02 00': [Email('dr1')],
                '03 00': [Email('dr2')],
                '04 00': [Email('dr3')],
            }),

            'drd': (0, {
                '02 00': [Email('dr1'), CreateGoal()],
                '02 18': [TrackStep(), CreateStep()],
                '04 00': [Email('d1', 2)],
                '04 12': [TrackStep(), CreateStep()],
                '06 00': [Email('d2', 1)],
            }),

            'drd2': (0, {
                '01 00': [CreateGoal()],
                '03 00': [Email('dr1'), CreateStep()],
                '03 18': [TrackStep(), CreateStep()],
                '05 00': [Email('d1', 2)],
                '06 00': [Email('d2', 1)],
                '07 00': [Email('d3', 0)],
            }),

            # 'h': (0, {
            #     '01 00': [CreateGoal(), CreateStep()],
            #     '01 06': [TrackStep(), CreateStep()],
            #     '01 18': [TrackStep(), CreateStep()],
            #     '02 06': [TrackStep(), CreateStep()],
            #     '02 18': [TrackStep(), CreateStep()],
            #     '03 06': [TrackStep(), Complete()],
            # }),
            #
            # 'hd': (0, {
            #     '01 00': [CreateGoal(), CreateStep()],
            #     '01 18': [TrackStep(), CreateStep()],
            #     '02 18': [TrackStep(), CreateStep()],
            #     '03 18': [Email('d1', 2)],
            #     '04 18': [Email('d2', 1)],
            #     '05 18': [Email('d3', 0)],
            # }),
            #
            # 'hdh': (0, {
            #     '01 00': [CreateGoal()],
            #     '01 12': [CreateStep()],
            #     '02 06': [TrackStep(), CreateStep()],
            #     '03 06': [Email('d1', 2)],
            #     '03 12': [TrackStep(), CreateStep()],
            #     '04 06': [TrackStep(), CreateStep()],
            #     '05 06': [Email('d2', 1)],
            #     '05 12': [TrackStep(), CreateStep()],
            # }),
            #
            # 'hdh2': (0, {
            #     '01 00': [CreateGoal(), CreateStep()],
            #     '01 18': [TrackStep()],
            #     '02 18': [Email('d1', 2)],
            #     '03 00': [CreateStep()],
            #     '03 18': [TrackStep(), CreateStep()],
            #     '04 12': [TrackStep(), CreateStep()],
            #     '05 06': [TrackStep(), CreateStep()],
            # })
        }

        hours = 0
        current_time = '01 00'

        users = {name: UserJourneyTest.User.register(name + '@t.com')
                 for name in spec.keys()}

        self.assertInbox([('n1_registration', user.email)
                          for name, user in users.items()])

        while hours <= 144:
            decimal_time = hours / 24
            quotient = decimal_time - math.floor(decimal_time)
            current_time = '0%d %02d' % \
                           (math.floor(decimal_time) + 1, quotient * 24)

            print('============ time=%s (%dh) ============' %
                  (current_time, hours))

            emails = []

            for name, (tz_offset, timeline) in spec.items():
                if current_time not in timeline:
                    continue

                user = users[name]

                actions = [event for event in timeline[current_time]
                           if isinstance(event, Action)]

                for action in actions:
                    email = action.do(user)

                    if email:
                        emails.append((email, user.email))

            self.send_dr_emails()
            self.send_d_emails()

            for name, (tz_offset, timeline) in spec.items():
                if current_time not in timeline:
                    continue

                user = users[name]

                for email in [e for e in timeline[current_time]
                              if isinstance(e, Email)]:
                    if user.goal:
                        user.goal.refresh_from_db()

                        msg = '%s should have %d lives after %s but has %d'\
                              % (user.email, email.lives, email.name,
                                 user.goal.lives)
                        self.assertEquals(email.lives, user.goal.lives, msg)

                    emails.append((email.name, user.email))

            self.assertInbox(emails)

            hours += 6
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

            self.client.post(reverse('new_goal'), data={
                'text': 'test goal',
                'first_step': 'test_step',
                'tz_offset': 0,
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
