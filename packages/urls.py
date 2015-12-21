from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.packages, name='package_list'),
    url(r'^insert_vouchers/$', views.insert_vouchers, name='insert_vouchers'),
]
