from django.test import TestCase
from django.conf import settings
from os import listdir
from os.path import isfile, join
from app import fixtures

from app.utils import render_email


class EmailTemplatesTest(TestCase):
    def test_templates(self):
        step = fixtures.step()
        goal = step.goal

        template_dir = join(settings.BASE_DIR, 'app/templates/emails')
        files = [f for f in listdir(template_dir)
                 if isfile(join(template_dir, f)) and f != 'base.html']

        if not files:
            self.fail('No email templates found')

        for file in files:
            name = file[:-5]

            print('Testing email ' + name)

            try:
                (html, text) = render_email(name, goal.user, goal)
            except Exception as e:
                print(e)
                self.fail('Failed to render %s email' % name)

            self.assertTrue('deactivate' in html)
            self.assertTrue('9141465' in html)
