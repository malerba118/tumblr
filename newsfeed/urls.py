from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#include((pattern_list, app_namespace, instance_namespace))
urlpatterns = patterns('',
    url(r'^$', 'newsfeed.views.newsfeed_view', name="newsfeed"),
    url(r'^posts/load/', 'newsfeed.views.load_more_posts', name="load-more-posts"),

)