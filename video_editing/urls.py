from django.conf.urls import patterns, url

from .basic_navigation import api
from .basic_navigation import views

urlpatterns = patterns('',
    url(r'^crop/(?P<video_name>\w+)/', views.crop, name='crop'),
)
