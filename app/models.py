from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Goal(models.Model):
    user = models.ForeignKey(User)

    text = models.TextField(max_length=144)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.id is None:
            self.end = self.start + timedelta(days=5)

        super(Goal, self).save(*args, **kwargs)


class Step(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

    text = models.TextField(max_length=144)
    start = models.DateTimeField()
    end = models.DateTimeField()

    complete = models.BooleanField()
    comments = models.TextField(max_length=144)
