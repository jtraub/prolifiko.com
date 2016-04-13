from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import uuid


class Goal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    text = models.TextField(max_length=144)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.id is None:
            self.end = self.start + timedelta(days=5)

        super(Goal, self).save(*args, **kwargs)


class Step(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

    text = models.TextField(max_length=144)
    start = models.DateTimeField()
    end = models.DateTimeField()

    complete = models.BooleanField()
    comments = models.TextField(max_length=144)
