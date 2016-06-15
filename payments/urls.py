from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<package_pk>\d+)/$', views.index, name='index'),
]
