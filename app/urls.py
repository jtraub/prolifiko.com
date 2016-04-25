from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import *
from .views import goals, steps


urlpatterns = [
    url(r'login/$', auth_views.login, name='app_login'),
    url(r'register/$', register, name='app_register'),

    url(r'goals/new/$', goals.new, name='app_goals_new'),

    url(r'goals/(?P<goal_id>[^/]+)/$',
        goals.timeline, name='app_goals_timeline'),

    url(r'goals/(?P<goal_id>[^/]+)/steps/new/$',
        steps.new, name='app_steps_new'),
    url(r'goals/(?P<goal_id>[^/]+)/steps/(?P<step_id>[^/]+)/start/$',
        steps.start, name='app_steps_start'),
    url(r'goals/(?P<goal_id>[^/]+)/steps/(?P<step_id>[^/]+)/track/$',
        steps.track, name='app_steps_track'),
    url(r'goals/(?P<goal_id>[^/]+)/steps/(?P<step_id>[^/]+)/complete/$',
        steps.complete, name='app_steps_complete'),
    url(r'goals/(?P<goal_id>[^/]+)/steps/(?P<step_id>[^/]+)/$',
        steps.update, name='app_steps_update'),

    url(r'goals/(?P<goal_id>[^/]+)/steps/(?P<step_id>[^/]+)/congrats/$',
        steps.update, name='app_steps_congrats'),

    url(r'^$', index, name='app_index'),
]
