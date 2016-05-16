from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from os import listdir
from os.path import join, isfile

from .models import Goal
from .utils import render_email


class EmailTemplateTest(TestCase):
    fixtures = ['users', 'goals']

    def test_templates(self):
        user = User.objects.get(username='test')
        goal = Goal.objects.all().first()
        context = {'goal': goal}

        dir = join(settings.BASE_DIR, 'app/templates/emails')
        templates = [f.replace('.html', '')
                     for f in listdir(dir) if isfile(join(dir, f))]

        for name in templates:
            try:
                render_email(name, user, context)
            except Exception:
                self.fail('Failed to render %s email' % name)
