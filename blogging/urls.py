from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#include((pattern_list, app_namespace, instance_namespace))
urlpatterns = patterns('',
	url(r'^(?P<slug>[-_\w]+)/', 'blogging.views.blog_view', name="blog"),

)