from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#include((pattern_list, app_namespace, instance_namespace))
urlpatterns = patterns('',
	url(r'^post/(?P<post_id>\d+)/reblog/', 'blogging.views.reblog_post', name="reblog"),
    url(r'^post/(?P<post_id>\d+)/like/', 'blogging.views.like', name="like"),
    url(r'^post/(?P<post_id>\d+)/unlike/', 'blogging.views.unlike', name="unlike"),
    url(r'^posts/tagged/(?P<tag>[-_\w]+)/', 'blogging.views.tagged_view', name="tagged"),
    url(r'^blog/(?P<slug>[-_\w]+)/post/create/', 'blogging.views.post_create_view', name="post-create"),
    url(r'^blog/(?P<slug>[-_\w]+)/edit/', 'blogging.views.blog_edit_view', name="blog-edit"),
    url(r'^blog/(?P<slug>[-_\w]+)/follow/', 'blogging.views.follow', name="follow"),
    url(r'^blog/(?P<slug>[-_\w]+)/unfollow/', 'blogging.views.unfollow', name="unfollow"),
    url(r'^blogs/browse/', 'blogging.views.blog_browse_view', name="blog-browse"),
	url(r'^blog/(?P<slug>[-_\w]+)/', 'blogging.views.blog_view', name="blog"),

)