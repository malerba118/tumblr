from django.core.context_processors import csrf
from django.shortcuts import render, get_object_or_404

# Create your views here.
from blogging.models import Blog


def blog_view(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    context = {"blog":blog}
    context.update(csrf(request))
    if blog.isOwnedBy(request.user):
        return render(request, "blog_edit.html", context)
    else:
        return render(request, blog.template, context)
