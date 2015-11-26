from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views
from .forms import ResetPasswordForm, PasswordResetEmailForm, LoginForm

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/accounts/login/'}, name='logout'),
    url(r'^password_change/$', auth_views.password_change, name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset, {
      'template_name': 'accounts/password_reset.html',
      'post_reset_redirect': '/accounts/password_reset/done/',
      'email_template_name': 'accounts/password_reset_email.html',
      'password_reset_form': PasswordResetEmailForm,
      'subject_template_name': 'accounts/password_reset_subject.txt'
    }, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'accounts/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {
      'post_reset_redirect': '/accounts/reset/done/',
      'template_name': 'accounts/password_reset_confirm.html',
      'set_password_form': ResetPasswordForm
    }, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^verify/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.verify_email, {}, name='verify_email'),
    url(r'^toggle_status/(?P<pk>\d+)/$', views.toggle_status, name='toggle_status'),
    url(r'^edit_user/(?P<pk>\d+)/$', views.edit_user, name='edit_user'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^upload_user_list/$', views.upload_user_list, name='upload_user_list'),
    url(r'^recharge/$', views.recharge_account, name='recharge_account'),
    url(r'^buy_package/$', views.buy_package, name='buy_package'),
    url(r'^users/$', views.view_users, name='users'),
    url(r'^users/add/$', views.add_user, name='add_user'),
]
