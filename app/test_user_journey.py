from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings
from django.contrib.auth.models import User
import logging

from .models import Goal


logger = logging.getLogger('prolifiko.app.test_user_journey')


class UserJourneyTest(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(DEBUG=True)
    def test_user_journey(self):
        ######################################################################
        # Register
        ######################################################################

        logger.debug('Registering as user@test.com')

        self.client.post(reverse('app_register'), {
            'email': 'user@test.com',
            'password1': 'test',
            'password2': 'test',
        })

        user = User.objects.get(email='user@test.com')

        ######################################################################
        # Receive N1
        ######################################################################

        self.assertEquals(1, len(mail.outbox))
        self.assertEmail('n1_registration', mail.outbox.pop())

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

        goal = Goal.objects.filter(user__email='user@test.com').first()

        ######################################################################
        # Create 1st step
        ######################################################################

        first_step = self.create_step('first step', goal)

        ######################################################################
        # Receive N2
        ######################################################################

        self.assertEquals(1, len(mail.outbox))
        self.assertEmail('n2_new_goal', mail.outbox.pop())

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
        self.assertEmail('n3_step_1_complete', mail.outbox.pop())

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
        self.assertEmail('n4_step_2_complete', mail.outbox.pop())

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
        self.assertEmail('n5_step_3_complete', mail.outbox.pop())

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
        self.assertEmail('n6_step_4_complete', mail.outbox.pop())

        ######################################################################
        # Track 5th step
        ######################################################################

        self.track_step(fifth_step)

        ######################################################################
        # Receive N7
        ######################################################################

        self.assertEquals(1, len(mail.outbox))
        self.assertEmail('n7_goal_complete', mail.outbox.pop())

        # Track 2nd step and set 3rd
        # Get N4

        # Track 3rd step and set 4th
        # Get N5

        # Track 4th step and set 5th
        # Get N6

        # Track 5th step
        # Get N7

        pass

    def assertEmail(self, name, email):
        self.assertEquals(settings.EMAIL_META[name]['subject'], email.subject)

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

        self.client.post(reverse('app_steps_track', kwargs={
            'goal_id': step.goal.id, 'step_id': step.id}))
