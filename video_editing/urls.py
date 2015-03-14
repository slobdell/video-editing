from django.conf.urls import patterns, url

from .basic_navigation import views

urlpatterns = patterns('',
    url(r'^crop/(?P<video_name>\w+)/', views.crop, name='crop'),
    url(r'^trim/(?P<video_name>\w+)/', views.trim, name='trim'),
    url(r'^trimreverse/(?P<video_name>\w+)/', views.trimreverse, name='trimreverse'),
    url(r'^self/(?P<video_name>\w+)/', views.local_review, name='crop'),
    url(r'^self/', views.local_review, name='blah'),
    url(r'^selftrim/(?P<video_name>\w+)/', views.trim_review, name='selftrim'),
    url(r'^selftrim/', views.trim_review, name='selftrim'),
    url(r'^secretreview/', views.secret_review, name='secret-review'),
)
