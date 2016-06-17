from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.packages, name='package_list'),
    url(r'^buy/$', views.buy_package, name='buy'),
    url(r'^insert/$', views.insert_stub, name='insert_stub'),
    url(r'^delete/$', views.delete_stub, name='delete_stub'),
    url(r'^insert_vouchers/$', views.insert_vouchers, name='insert_vouchers'),
    url(r'^create_subscription/(?P<package_pk>\d+)/$', views.create_subscription, name='create_subscription'),
]
