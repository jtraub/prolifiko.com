from django.test import TestCase
from django.conf import settings
from os import listdir
from os.path import isfile, join

from app.utils import render_email
from app.models import Goal, Step


class EmailTemplatesTest(TestCase):
    fixtures = ['users', 'goals']

    def test_templates(self):
        goal = Goal.objects.first()
        Step.create(goal, 'test')

        template_dir = join(settings.BASE_DIR, 'app/templates/emails')
        files = [f for f in listdir(template_dir)
                 if isfile(join(template_dir, f)) and f != 'base.html']

        if not files:
            self.fail('No email templates found')

        for file in files:
            name = file[:-5]

            print('Testing email ' + name)

            try:
                render_email(name, goal.user, goal)
            except Exception as e:
                print(e)
                self.fail('Failed to render %s email' % name)
