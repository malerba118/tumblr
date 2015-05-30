from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#include((pattern_list, app_namespace, instance_namespace))
urlpatterns = patterns('',
    url(r'^(?P<slug>[-_\w]+)/post/create/', 'blogging.views.post_create_view', name="post-create"),
	url(r'^post/(?P<post_id>\d+)/reblog/', 'blogging.views.reblog_post', name="reblog"),
    url(r'^post/(?P<post_id>\d+)/like/', 'blogging.views.like', name="like"),
    url(r'^post/(?P<post_id>\d+)/unlike/', 'blogging.views.unlike', name="unlike"),
    url(r'^(?P<slug>[-_\w]+)/follow/', 'blogging.views.follow', name="follow"),
	url(r'^(?P<slug>[-_\w]+)/', 'blogging.views.blog_view', name="blog"),

)