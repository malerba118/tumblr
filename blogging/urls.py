from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#include((pattern_list, app_namespace, instance_namespace))
urlpatterns = patterns('',
    url(r'^likes/refresh/(?P<post_id>\d+)/', 'blogging.views.likes_refresh_ajax', name="likes-refresh"),
	url(r'^post/(?P<post_id>\d+)/reblog/', 'blogging.views.reblog_post', name="reblog"),
    url(r'^post/(?P<post_id>\d+)/like/', 'blogging.views.like_toggle', name="like"),
    url(r'^post/(?P<post_id>\d+)/delete/', 'blogging.views.post_delete_ajax', name="post-delete"),
    url(r'^posts/tagged/(?P<tag>[-_\w]+)/posts/load/', 'blogging.views.load_more_tagged_posts', name="load-more-tagged-posts"),
    url(r'^posts/tagged/(?P<tag>[-_\w]+)/', 'blogging.views.tagged_view', name="tagged"),
    url(r'^blog/(?P<slug>[-_\w]+)/post/create/', 'blogging.views.post_create_view', name="post-create"),
    url(r'^blog/(?P<slug>[-_\w]+)/edit/', 'blogging.views.blog_edit_view', name="blog-edit"),
    url(r'^blog/(?P<slug>[-_\w]+)/follow/', 'blogging.views.follow', name="follow"),
    url(r'^blog/(?P<slug>[-_\w]+)/unfollow/', 'blogging.views.unfollow', name="unfollow"),
    url(r'^blog/(?P<slug>[-_\w]+)/posts/load/', 'blogging.views.load_more_blog_posts', name="load-more-blog-posts"),
    url(r'^blogs/browse/', 'blogging.views.blog_browse_view', name="blog-browse"),
	url(r'^blog/(?P<slug>[-_\w]+)/', 'blogging.views.blog_view', name="blog"),

)