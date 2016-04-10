from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import *
from .views import goals


urlpatterns = [
    url(r'login/$', auth_views.login, name='app_login'),
    url(r'register/$', register, name='app_register'),

    url(r'goals/new/$', goals.new, name='app_goals_new'),

    url(r'^$', index, name='app_index'),
]
