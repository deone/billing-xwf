from django.conf.urls import include, url
from django.contrib import admin

from accounts import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^captive/$', views.captive, name='captive'),
    url(r'^success/$', views.success, name='success'),
    url(r'^resend_mail/$', views.resend_mail, name='resend_mail'),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^packages/', include('packages.urls', namespace="packages")),
    url(r'^admin/', include(admin.site.urls)),
]
