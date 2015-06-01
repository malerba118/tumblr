from django.contrib import messages
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from blogging.forms import PostCreateForm, BlogEditForm
from blogging.models import Blog, Post, Like, Tag, Activity, POST, REBLOG, FOLLOW, Follow
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
    context = {"blog":blog,
               "posts":posts,
               "is_following":is_following,
               "base_template":base_template,
               "has_edit_permissions":has_edit_permissions}
    context.update(csrf(request))
    return render(request, blog.template, context)


def blog_edit_view(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if not blog.isOwnedBy(request.user):
        return HttpResponseForbidden()

    form = BlogEditForm(request.POST or None, instance=blog)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(blog.get_absolute_url())
        #else:
            #messages.error(request, "This blog name is already taken!")

    context = {"form":form}
    context.update(csrf(request))
    return render(request, "blog_edit.html", context)




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
    form.fields["content"].initial = "<blockquote>%s</blockquote><a href='%s'>%s:</a>" % \
                                     (post.content, request.user.blog.slug, request.user.blog.slug)
    context = {"post_form": form}
    context.update(csrf(request))
    return render(request, "post_create.html", context)


def follow(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if not request.user.blog.is_following(blog):
        follow = request.user.blog.follow(blog)
        Activity.create_activity(request.user.blog, follow, FOLLOW)
    return redirect(reverse("blog", kwargs={"slug":blog.slug}))

def unfollow(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.user.blog.is_following(blog):
        follow = Follow.objects.get(follower=request.user.blog, followee=blog)
        follow.delete()
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


def tagged_view(request, tag):
    posts = Tag.find_posts_for_tag(tag)
    post_dicts=[]
    for post in posts:
        post_dicts.append({"post": post,
                           "is_liked":post.is_liked_by(request.user.blog),
                           "reblogs": post.find_notes(),
                           "likes": post.find_likes(),
                           "tags": post.tags.all()})
    context = {"tag":tag, "post_dicts":post_dicts}
    return render(request, "tagged.html", context)


class DisplayInfo():

    def __init__(self, subject, object, activity_type):
        self["activity_type"] = activity_type
        self["timestamp"] = object.timestamp

    def is_post(self):
        return self.activity_type == POST

class PostDisplayInfo(DisplayInfo):

    def __init__(self, subject, post, activity_type):
        DisplayInfo.__init__(self, subject, post, activity_type)
        self["post"] = post
        self["is_liked"] = post.is_liked_by(subject)
        self["reblogs"] = post.find_notes()
        self["tags"] = post.tags.all()