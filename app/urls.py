from django.conf.urls import url
from django.contrib.auth import views as django_auth

from .forms import SetPasswordForm
from .views import index, auth, goals, steps, account, test, menu

password_reset_kwargs = {
    'email_template_name': 'registration/password_reset_email.txt',
    'html_email_template_name': 'registration/password_reset_email.html'
}

urlpatterns = [
    url(r'login/$', auth.login, name='app_login'),
    url(r'register/$', auth.register, name='app_register'),

    url(r'users/(?P<user_id>[^/]+)/deactivate/$',
        account.deactivate, name='app_deactivate'),

    url(r'account/reset_password/$',
        django_auth.password_reset,
        name='password_reset',
        kwargs=password_reset_kwargs),
    url(r'account/reset_password/done/$',
        django_auth.password_reset_done, name='password_reset_done'),
    url(r'^account/reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        django_auth.password_reset_confirm,
        name='password_reset_confirm',
        kwargs={'set_password_form': SetPasswordForm}),
    url(r'^reset/done/$',
        django_auth.password_reset_complete, name='password_reset_complete'),


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

    url(r'^about/$', menu.about, name='app_menu_about'),
    url(r'^terms/$', menu.terms,  name='app_menu_terms'),
    url(r'^privacy/$', menu.privacy, name='app_menu_privacy'),
    url(r'^help/$', menu.help, name='app_menu_help'),

    url(r'test/render_email/(?P<name>[^/]+)/$', test.render_email)
]
