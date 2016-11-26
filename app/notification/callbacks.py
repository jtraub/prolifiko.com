from django.db import transaction
from django.utils import timezone
from app.models import Step, Email


def late_step_success(item, notifier_output, now=None):
    # we proceed only after successful email notification about a late step
    if not(isinstance(item, Step) and isinstance(notifier_output, Email)):
        return notifier_output

    # take a life
    # save Email object to the database in the same transaction
    now = timezone.now()

    with transaction.atomic():
        item.lose_life(now)
        notifier_output.step = item
        notifier_output.save()

    return notifier_output


def late_step_failure(item, exception):
    # log failure ?
    pass
