from django.conf.urls import url

from .views import index, auth, goals, steps


urlpatterns = [
    url(r'login/$', auth.login, name='app_login'),
    url(r'register/$', auth.register, name='app_register'),

    url(r'goals/new/$', goals.new, name='app_goals_new'),

    url(r'goals/(?P<goal_id>[^/]+)/$',
        goals.timeline, name='app_goals_timeline'),
    url(r'goals/(?P<goal_id>[^/]+)/complete/$',
        goals.complete, name='app_goals_complete'),

    url(r'goals/(?P<goal_id>[^/]+)/steps/new/$',
        steps.new, name='app_steps_new'),
    url(r'goals/(?P<goal_id>[^/]+)/steps/(?P<step_id>[^/]+)/start/$',
        steps.start, name='app_steps_start'),
    url(r'goals/(?P<goal_id>[^/]+)/steps/(?P<step_id>[^/]+)/track/$',
        steps.track, name='app_steps_track'),

    url(r'^$', index, name='app_index'),
]
