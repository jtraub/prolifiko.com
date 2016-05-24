from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel
import uuid
from .utils import nth


class Goal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    text = models.TextField(max_length=144)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()

    lives = models.IntegerField(default=3)

    def __str__(self):
        return '%s (%s)' % (self.id, self.user.email)

    def save(self, *args, **kwargs):
        if self.end is None:
            self.end = self.start + timedelta(days=5)

        super(Goal, self).save(*args, **kwargs)

    def lose_life(self, commit=False):
        self.lives -= 1
        if commit:
            self.save()


class Step(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    goal = models.ForeignKey(Goal, related_name='steps',
                             on_delete=models.CASCADE)

    text = models.TextField(max_length=144)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()

    complete = models.BooleanField(default=False)
    comments = models.TextField(max_length=144, blank=True)

    class Meta:
        ordering = ('start',)

    @staticmethod
    def create(goal: Goal, text: str):
        start = timezone.now()
        end = start + timedelta(days=1)

        return Step.objects.create(
            goal=goal,
            text=text,
            start=start,
            end=end
        )

    @property
    def number(self):
        if not hasattr(self, '_number'):
            self._number = list(self.goal.steps.all()).index(self) + 1

        return self._number

    @property
    def nth(self):
        return nth[self.number]


@register_snippet
class Email(models.Model):
    name = models.TextField()
    user_journey_ref = models.TextField()
    content = RichTextField()
    subject = models.TextField()

    panels = [
        FieldRowPanel([
            FieldPanel('name', classname='col6'),
            FieldPanel('user_journey_ref', classname='col6')
        ]),
        FieldPanel('subject'),
        FieldPanel('content', classname='full')
    ]
