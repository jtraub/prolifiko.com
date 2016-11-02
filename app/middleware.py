from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def maintenance_middleware(get_response):
    def is_test_user(user):
        if user.email in settings.TEST_EMAIL_ADDRESSES:
            return False

        for domain in settings.TEST_EMAIL_DOMAINS:
            if user.email.endswith(domain):
                return False

        return True

    def middleware(request):
        if settings.MAINTENANCE_MODE:
            if not request.user.is_authenticated():
                return get_response(request)

            # Allow users to get to the login page so that staff users
            # can login
            if request.path == reverse('login'):
                return get_response(request)

            # Let staff and testers do anything
            if request.user.is_staff or is_test_user(request.user):
                return get_response(request)

            # Passthru for the maintenance page
            if request.path == reverse('maintenance'):
                return get_response(request)

        return redirect(reverse('maintenance'))

    return middleware
