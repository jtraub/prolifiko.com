from django.conf.urls import url
from django.contrib.auth import views as django_auth

from .forms import SetPasswordForm
from .views import index, auth, goals, steps, account, test, menu, maintenance

password_reset_kwargs = {
    'email_template_name': 'registration/password_reset_email.txt',
    'html_email_template_name': 'registration/password_reset_email.html'
}

urlpatterns = [
    url(r'login/$', auth.login, name='login'),
    url(r'register/$', auth.register, name='register'),
    url(r'welcome/$', auth.welcome, name='welcome'),

    url(r'users/(?P<user_id>[^/]+)/deactivate/$',
        account.deactivate, name='deactivate'),

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

    url(r'^$', index, name='myprogress'),

    url(r'goals/new/$', goals.new, name='new_goal'),

    url(r'goals/(?P<goal_id>[^/]+)/$',
        goals.timeline, name='goal_progress'),
    url(r'goals/(?P<goal_id>[^/]+)/complete/$',
        goals.complete, name='complete_goal'),

    url(r'goals/(?P<goal_id>[^/]+)/steps/new/$',
        steps.new, name='new_step'),
    url(r'goals/(?P<goal_id>[^/]+)/steps/latest/$',
        steps.latest, name='latest_step'),
    url(r'goals/(?P<goal_id>[^/]+)/steps/(?P<step_id>[^/]+)/start/$',
        steps.start, name='start_step'),
    url(r'goals/(?P<goal_id>[^/]+)/steps/(?P<step_id>[^/]+)/track/$',
        steps.track, name='complete_step'),

    url(r'^about/$', menu.about, name='menu_about'),
    url(r'^terms/$', menu.terms,  name='menu_terms'),
    url(r'^privacy/$', menu.privacy, name='menu_privacy'),
    url(r'^help/$', menu.help, name='menu_help'),

    url(r'test/render_email/(?P<name>[^/]+)/$', test.render_email),

    url(r'maintenance/$', maintenance, name='maintenance'),
]
