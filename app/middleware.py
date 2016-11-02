from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from app.utils import get_logger

logger = get_logger(__name__)


def maintenance_middleware(get_response):
    def is_test_user(user):
        if user.email in settings.TEST_EMAIL_ADDRESSES:
            return True

        for domain in settings.TEST_EMAIL_DOMAINS:
            if user.email.endswith(domain):
                return True

        return False

    def middleware(request):
        if settings.MAINTENANCE_MODE:
            logger.debug('Maintenance mode active request.path=%s' %
                         request.path)

            # Allow users to get to the login page so that staff users
            # can login
            if request.path == reverse('login') \
                    or request.path == reverse('register'):
                logger.debug('Passthru login/register page')
                return get_response(request)

            if not request.user.is_authenticated():
                logger.debug('Not logged in, redirecting to login')
                return redirect('login')

            # Passthru for the maintenance page
            if request.path == reverse('maintenance'):
                logger.debug('Passthru maintenance page')
                return get_response(request)

            # Let staff and testers do anything
            if request.user.is_staff or is_test_user(request.user):
                logger.debug('Permitting staf/test user email=%s' %
                             request.user.email)
                return get_response(request)

            logger.debug('Redirecting to maintenance page')
            return redirect(reverse('maintenance'))

        return get_response(request)

    return middleware
