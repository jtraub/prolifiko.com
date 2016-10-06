from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def maintenance_middleware(get_response):
    def is_user(user):
        if user.email in settings.TEST_EMAIL_ADDRESSES:
            return False

        for domain in settings.TEST_EMAIL_DOMAINS:
            if user.email.endswith(domain):
                return False

        return True

    def middleware(request):
        if settings.MAINTENANCE_MODE:
            if request.path == reverse('maintenance'):
                return get_response(request)

            if request.path == reverse('app_login')\
                    or request.path == reverse('app_register'):
                return redirect('maintenance')

            if request.user.is_authenticated() and is_user(request.user):
                return redirect('maintenance')

        return get_response(request)

    return middleware
