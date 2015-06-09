from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.text import slugify


@login_required(login_url='/auth/login/')
def search_tags(request):
    query = request.GET['q']
    if query != None:
        tag = slugify(query)
        if tag != '':
            return redirect(reverse("tagged", kwargs={"tag":tag}))
    return redirect(request.META.get('HTTP_REFERER'))
