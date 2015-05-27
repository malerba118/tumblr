from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#include((pattern_list, app_namespace, instance_namespace))
urlpatterns = patterns('',
	url(r'^register/', 'authentication.views.register', name="register"),
	#url(r'^login/', 'authentication.views.log_in', name='log-in'),
	#url(r'^logout/', 'authentication.views.log_out', name='log-out'),


)