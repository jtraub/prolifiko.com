from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'user_journey/$', views.user_journey),
    url(r'active_users/$', views.active_users),
]
