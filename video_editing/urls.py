from django.conf.urls import patterns, url

from .basic_navigation import api
from .basic_navigation import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^api/submit/', api.submit, name="submit"),
)
