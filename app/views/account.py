from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.models import User
from app.utils import get_logger, add_event

logger = get_logger(__name__)


def deactivate(request, user_id):
    try:
        user = User.objects.get(pk=int(user_id))
    except User.DoesNotExist:
        return HttpResponseBadRequest()

    if user.is_active:
        logger.info('Deactivating user ' + user.email)

        add_event('deactivate', {
            'id': user.id,
            'email': user.email
        })

        user.is_active = False
        user.save()

    return render(request, 'account/deactivated.html')
