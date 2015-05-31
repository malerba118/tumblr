from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.text import slugify



def search_tags(request):
    query = request.GET['q']
    if query != None:
        tag = slugify(query)
        if tag != '':
            return redirect(reverse("tagged", kwargs={"tag":tag}))
    return redirect(request.META.get('HTTP_REFERER'))
