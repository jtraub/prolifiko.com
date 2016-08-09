from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'reports/$', views.list_reports),
    url(r'reports/(?P<name>.+)/$', views.csv_report),
    url(r'user_journey/$', views.user_journey),
    url(r'active_users/$', views.active_users),
    url(r'user_history/$', views.user_history),
]
