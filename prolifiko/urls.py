from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'', include('app.urls')),
    url(r'metrics/', include('metrics.urls')),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
