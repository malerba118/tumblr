"""tumblr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import socket
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', "tumblr.views.home"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include("authentication.urls")),
    url(r'^blogging/', include("blogging.urls")),
    url(r'^newsfeed/', include("newsfeed.urls")),
    url(r'^search/', include("search.urls")),
    url(r'^summernote/', include('django_summernote.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if socket.gethostname() != "ip-172-31-17-54": #Dev server
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)