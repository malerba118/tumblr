from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from blogging.forms import PostCreateForm
from blogging.models import Blog, Post, Like, Tag
from newsfeed.models import *


def blog_view(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    posts = blog.get_posts()
    is_following = request.user.blog.is_following(blog)
    has_edit_permissions = blog.isOwnedBy(request.user)
    if has_edit_permissions:
        base_template = "editable_base_blog.html"
    else:
        base_template = "base_blog.html"
    context = {"blog":blog, "posts":posts, "is_following":is_following, "base_template":base_template}
    context.update(csrf(request))
    return render(request, blog.template, context)

def post_create_view(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if blog.isOwnedBy(request.user):
        post_form = PostCreateForm(request.POST or None)
        if request.method == "POST":
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.blog = blog
                post.root = None
                post.save()
                post.root = post
                post.tags = Tag.find_or_create_tags(post_form.data["tags_field"])
                post.save()
                Activity.create_activity(blog, post, POST)
                return redirect(blog.get_absolute_url())
        context = {"post_form":post_form}
        context.update(csrf(request))
        return render(request, "post_create.html", context)
    return HttpResponseForbidden()

def reblog_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.root = post.root
            new_post.blog = request.user.blog
            new_post.save()##must persist prior to setting tags field
            new_post.tags = Tag.find_or_create_tags(form.data["tags_field"])
            new_post.save()
            Activity.create_activity(request.user.blog, new_post, REBLOG)
            return redirect(request.user.blog.get_absolute_url())
    form = PostCreateForm()
    form.fields["title"].initial = post.title
    form.fields["content"].initial = post.content
    context = {"post_form": form}
    context.update(csrf(request))
    return render(request, "post_create.html", context)


def follow(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if not request.user.blog.is_following(blog):
        follow = request.user.blog.follow(blog)
        Activity.create_activity(request.user.blog, follow, FOLLOW)
    return redirect(reverse("blog", kwargs={"slug":blog.slug}))

def like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like = Like()
    like.liker = request.user.blog
    like.liked = post
    like.save()
    return redirect(request.META.get('HTTP_REFERER'))

def unlike(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like = get_object_or_404(Like, liker=request.user.blog, liked=post)
    like.delete()
    return redirect(request.META.get('HTTP_REFERER'))
