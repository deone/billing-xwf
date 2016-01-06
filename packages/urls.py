from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.packages, name='package_list'),
    url(r'^insert/$', views.insert_stub, name='insert_stub'),
    url(r'^delete/$', views.delete_stub, name='delete_stub'),
    url(r'^insert_vouchers/$', views.insert_vouchers, name='insert_vouchers'),
]
