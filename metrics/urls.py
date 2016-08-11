from django.conf.urls import url
from .views import metrics, reports, debug


urlpatterns = [
    url(r'conversion/$', metrics.conversion),
    url(r'reports/(?P<name>.+)/$', reports.csv_report),
    url(r'debug/active_users/$', debug.active_users),
    url(r'debug/user_history/$', debug.user_history),
    url(r'$', metrics.dashboard),
]
