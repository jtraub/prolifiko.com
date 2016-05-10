from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import uuid


class Goal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    text = models.TextField(max_length=144)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.end is None:
            self.end = self.start + timedelta(days=5)

        super(Goal, self).save(*args, **kwargs)


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
