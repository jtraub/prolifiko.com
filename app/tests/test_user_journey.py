from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from time import sleep
from unittest.mock import patch, Mock
import logging

from app.models import Goal, Step

DAY = 4
DAY_DELTA = {'seconds': DAY}

logger = logging.getLogger('prolifiko.app.test_user_journey')


@patch('django.core.mail.utils.socket')
class UserJourneyTest(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(DEBUG=True)
    def test_user_journey(self, socket):
        socket.getfqdn = Mock(return_value='test')

        ######################################################################
        # Register
        ######################################################################

        logger.debug('Registering as user@t.com')

        self.client.post(reverse('app_register'), {
            'email': 'user@t.com',
            'password1': 'test',
            'password2': 'test',
        })

        user = User.objects.get(email='user@t.com')

        ######################################################################
        # Receive N1
        ######################################################################

        self.assertEquals(1, len(mail.outbox))
        self.assertEmail('n1_registration', user)

        ######################################################################
        # Login
        ######################################################################

        self.client.login(username=user.username, password='test')

        ######################################################################
        # Create a Goal
        ######################################################################

        logger.debug('Creating a goal')

        self.client.post(reverse('app_goals_new'), data={
            'text': 'test goal',
        })

        self.assertEquals(0, len(mail.outbox))

        goal = Goal.objects.filter(user=user).first()

        ######################################################################
        # Create 1st step
        ######################################################################

        first_step = self.create_step('first step', goal)

        ######################################################################
        # Receive N2
        ######################################################################

        self.assertEquals(1, len(mail.outbox))
        self.assertEmail('n2_new_goal', user)

        ######################################################################
        # Track 1st step
        ######################################################################

        self.track_step(first_step)

        ######################################################################
        # Create 2nd step
        ######################################################################

        second_step = self.create_step('second step', goal)

        ######################################################################
        # Receive N3
        ######################################################################

        self.assertEquals(1, len(mail.outbox))
        self.assertEmail('n3_step_1_complete', user)

        ######################################################################
        # Track 2nd step
        ######################################################################

        self.track_step(second_step)

        ######################################################################
        # Create 3rd step
        ######################################################################

        third_step = self.create_step('third step', goal)

        ######################################################################
        # Receive N4
        ######################################################################

        self.assertEquals(1, len(mail.outbox))
        self.assertEmail('n4_step_2_complete', user)

        ######################################################################
        # Track 3rd step
        ######################################################################

        self.track_step(third_step)

        ######################################################################
        # Create 4th step
        ######################################################################

        fourth_step = self.create_step('fourth step', goal)

        ######################################################################
        # Receive N5
        ######################################################################

        self.assertEquals(1, len(mail.outbox))
        self.assertEmail('n5_step_3_complete', user)

        ######################################################################
        # Track 4rd step
        ######################################################################

        self.track_step(fourth_step)

        ######################################################################
        # Create 5th step
        ######################################################################

        fifth_step = self.create_step('fifth step', goal)

        ######################################################################
        # Receive N6
        ######################################################################

        self.assertEquals(1, len(mail.outbox))
        self.assertEmail('n6_step_4_complete', user)

        ######################################################################
        # Track 5th step
        ######################################################################

        complete = self.track_step(fifth_step)

        self.assertRedirects(complete, reverse('app_goals_complete',
                                               kwargs={'goal_id': goal.id}))

        ######################################################################
        # Complete
        ######################################################################

        self.client.post(reverse('app_goals_complete',
                                 kwargs={'goal_id': goal.id}))

        ######################################################################
        # Receive N7
        ######################################################################

        self.assertEquals(1, len(mail.outbox))
        self.assertEmail('n7_goal_complete', user)

        pass

    @override_settings(INACTIVE_TIME=DAY, INACTIVE_TIME_UNIT='seconds')
    def test_emails(self, socket):
        socket.getfqdn = Mock(return_value='test')
        from app.tasks import send_d_emails, send_dr_emails

        ######################################################################
        # Start
        # - All users join
        # - dr_user and dr_d_user do not set a goals
        # - d_user_1 and d_user_2 set a goal and first step
        #
        # End of Day 1
        # - dr_user and dr_d_user receive DR1
        # - d_user_1 does not track first step so receives D1
        # - d_user_2 completes first step and sets second
        #
        # End of Day 2
        # - dr_user receives DR2
        # - dr_d_user sets goal and first step
        # - d_user_1 receives D2
        # - d_user_2 does not track second step so receives D1
        #
        # End of Day 3
        # - dr_user receives DR3
        # - dr_d_user does not track first step and so receives D1
        # - d_user_1 receives D3
        # - d_user_2 tracks second step and sets third
        #
        # End of Day 4
        # - dr_d_user tracks first step and sets second
        # - d_user_2 does not track third step and so receives D2
        #
        # End of Day 5
        # - dr_d_user tracks second step and sets third
        # - d_user_2 receives D3
        ######################################################################

        start = timezone.now()
        logger.info('Start: %s' % start)

        ######################################################################
        # START
        ######################################################################

        # dr_user

        dr_user = User.objects.create(username='dr',
                                      email='dr@t.com',
                                      date_joined=start)

        dr_d_user = User.objects.create(username='dr_d',
                                        email='dr_d@t.com',
                                        date_joined=start)

        # d_user_1

        d_user_1 = User.objects.create(username='d1',
                                       email='d1@t.com',
                                       date_joined=start)

        d_user_1_goal = Goal.objects.create(user=d_user_1, text='test')

        Step.objects.create(
            goal=d_user_1_goal,
            text='test',
            end=start
        )

        # d_user_2

        d_user_2 = User.objects.create(username='d2',
                                       email='d2@t.com',
                                       date_joined=start)

        d_user_2_goal = Goal.objects.create(user=d_user_2, text='test')

        Step.objects.create(
            goal=d_user_2_goal,
            text='test',
            end=start
        )
        Step.objects.create(
            goal=d_user_2_goal,
            text='test',
            end=start + timedelta(seconds=DAY),
        )
        Step.objects.create(
            goal=d_user_2_goal,
            text='test',
            end=start + timedelta(seconds=DAY * 3),
        )

        # active_user

        active_user = User.objects.create(username='active',
                                          email='active@t.com',
                                          date_joined=start)

        active_user_goal = Goal.objects.create(user=active_user, text='test')
        Step.objects.create(
            goal=active_user_goal,
            text='test',
            end=start,
            complete=True,
        )
        Step.objects.create(
            goal=active_user_goal,
            text='test',
            end=start + timedelta(seconds=DAY),
            complete=True,
        )
        Step.objects.create(
            goal=active_user_goal,
            text='test',
            end=start + timedelta(seconds=DAY * 2),
            complete=True,
        )
        Step.objects.create(
            goal=active_user_goal,
            text='test',
            end=start + timedelta(seconds=DAY * 3),
            complete=True,
        )
        Step.objects.create(
            goal=active_user_goal,
            text='test',
            end=start + timedelta(seconds=DAY * 4),
            complete=True,
        )

        logger.debug('Day 0')

        ######################################################################
        # Day 1
        ######################################################################

        sleep(DAY/4)
        logger.debug('Day 0.25')
        send_d_emails()
        send_dr_emails()
        sleep(DAY / 4)
        logger.debug('Day 0.5')
        send_d_emails()
        send_dr_emails()
        sleep(DAY / 4)
        logger.debug('Day 0.75')
        send_d_emails()
        send_dr_emails()

        logger.debug('d2@t.com first step complete')
        d_user_2_first_step = d_user_2_goal.steps.first()
        d_user_2_first_step.complete = True
        d_user_2_first_step.save()

        sleep(DAY / 4)
        logger.debug('Day 1')
        send_d_emails()
        send_dr_emails()

        self.assertInbox(3)
        self.assertEmail('d1', d_user_1)
        self.assertEmail('dr1', dr_user)
        self.assertEmail('dr1', dr_d_user)

        ######################################################################
        # Day 2
        ######################################################################

        sleep(DAY / 4)
        logger.debug('Day 1.25')
        send_d_emails()
        send_dr_emails()
        sleep(DAY / 4)
        logger.debug('Day 1.5')
        send_d_emails()
        send_dr_emails()
        sleep(DAY / 4)
        logger.debug('Day 1.75')
        send_d_emails()
        send_dr_emails()

        logger.debug('dr_d@t.com sets goal and first step')
        dr_d_user_goal = Goal.objects.create(user=dr_d_user, text='test')
        dr_d_user_first_step = Step.objects.create(
            goal=dr_d_user_goal,
            text='test',
            end=start + timedelta(seconds=DAY * 2)
        )

        sleep(DAY / 4)
        logger.debug('Day 2')
        send_d_emails()
        send_dr_emails()

        self.assertInbox(3)
        self.assertEmail('d2', d_user_1)
        self.assertEmail('d1', d_user_2)
        self.assertEmail('dr2', dr_user)

        ######################################################################
        # Day 3
        ######################################################################

        sleep(DAY / 4)
        logger.debug('Day 2.25')
        send_d_emails()
        send_dr_emails()
        sleep(DAY / 4)
        logger.debug('Day 2.5')
        send_d_emails()
        send_dr_emails()
        sleep(DAY / 4)
        logger.debug('Day 2.75')
        send_d_emails()
        send_dr_emails()

        logger.debug('d2@t.com second step complete)')
        d_user_2_second_step = d_user_2_goal.steps.all()[1]
        d_user_2_second_step.complete = True
        d_user_2_second_step.save()

        sleep(DAY / 4)
        logger.debug('Day 3')
        send_d_emails()
        send_dr_emails()

        self.assertInbox(3)
        self.assertEmail('d3', d_user_1)
        self.assertEmail('d2', dr_d_user)
        self.assertEmail('dr3', dr_user)

        ######################################################################
        # Day 4
        ######################################################################

        sleep(DAY / 4)
        logger.debug('Day 3.25')
        send_d_emails()
        send_dr_emails()
        sleep(DAY / 4)
        logger.debug('Day 3.5')
        send_d_emails()
        send_dr_emails()
        sleep(DAY / 4)
        logger.debug('Day 3.75')
        send_d_emails()
        send_dr_emails()

        logger.debug('dr_d@t.com tracks first step and sets second')
        dr_d_user_first_step.complete = True
        dr_d_user_first_step.save()

        dr_d_user_second_step = Step.objects.create(
            goal=dr_d_user_goal,
            text='test',
            end=start + timedelta(seconds=DAY * 4)
        )

        sleep(DAY / 4)
        logger.debug('Day 4')
        send_d_emails()
        send_dr_emails()

        self.assertInbox(1)
        self.assertEmail('d2', d_user_2)

        ######################################################################
        # Day 5
        ######################################################################

        sleep(DAY / 4)
        logger.debug('Day 4.25')
        send_d_emails()
        send_dr_emails()
        sleep(DAY / 4)
        logger.debug('Day 4.5')
        send_d_emails()
        send_dr_emails()
        sleep(DAY / 4)
        logger.debug('Day 4.75')
        send_d_emails()
        send_dr_emails()

        logger.debug('dr_d@t.com tracks first step and sets second')
        dr_d_user_second_step.complete = True
        dr_d_user_second_step.save()

        Step.objects.create(
            goal=dr_d_user_goal,
            text='test',
            end=start + timedelta(seconds=DAY * 5)
        )

        sleep(DAY / 4)
        logger.debug('Day 5')
        send_d_emails()
        send_dr_emails()

        self.assertInbox(1)
        self.assertEmail('d3', d_user_2)

    def assertEmail(self, name, user):
        if len(mail.outbox) == 0:
            self.fail('No emails in outbox')

        email = mail.outbox.pop(0)

        self.assertEquals(user.email, email.to[0], name)
        self.assertEquals(name, email.prolifiko_name, name)

    def assertInbox(self, unread):
        self.assertEquals(unread, len(mail.outbox), [
            (email.prolifiko_name, email.to[0]) for email in mail.outbox
        ])

    def create_step(self, text, goal):
        logger.debug('Creating ' + text)

        self.client.post(
            reverse('app_steps_new', kwargs={'goal_id': goal.id}),
            data={'text': text},
        )

        goal.refresh_from_db()
        return goal.steps.last()

    def track_step(self, step):
        logger.debug('Tracking ' + step.text)

        return self.client.post(reverse('app_steps_track',
                                        kwargs={
                                            'goal_id': step.goal.id,
                                            'step_id': step.id}))
