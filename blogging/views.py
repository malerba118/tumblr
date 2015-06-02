from django.contrib import messages
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from blogging.forms import PostCreateForm, BlogEditForm
from blogging.models import Blog, Post, Like, Tag, Activity, POST, REBLOG, FOLLOW, Follow, LIKE
from newsfeed.models import *


def blog_view(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    posts = blog.get_posts()
    is_following = request.user.blog.is_following(blog)
    has_edit_permissions = blog.isOwnedBy(request.user)
    followers = blog.find_followers()
    follower_info_list = [BlogDisplayInfo(blog, follower) for follower in followers]
    followees = blog.find_followees()
    followee_info_list = [BlogDisplayInfo(blog, followee) for followee in followees]
    context = {"blog":blog,
               "posts":posts,
               "is_following":is_following,
               "has_edit_permissions":has_edit_permissions,
               "follower_info_list":follower_info_list,
               "followee_info_list":followee_info_list
    }
    context.update(csrf(request))
    return render(request, blog.template, context)


def blog_edit_view(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if not blog.isOwnedBy(request.user):
        return HttpResponseForbidden()

    form = BlogEditForm(request.POST or None, request.FILES or None, instance=blog)
    if request.method == "POST":
        if form.is_valid():
            updated_blog = form.save(commit=False)

            updated_blog.save()
            return redirect(blog.get_absolute_url())
        #else:
            #messages.error(request, "This blog name is already taken!")

    context = {"form":form}
    context.update(csrf(request))
    return render(request, "blog_edit.html", context)


def blog_browse_view(request):
    blogs = Blog.objects.all().order_by('?')[:150]
    display_info_list = (BlogDisplayInfo(request.user.blog, blog) for blog in blogs)
    return render(request, "blog_browse.html", {"display_info_list":display_info_list})

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
    form.fields["content"].initial = "<blockquote>" + post.content+ '</blockquote>' + '<a href="' +request.user.blog.get_absolute_url()+ '">' + request.user.blog.slug + "</a>"
    context = {"post_form": form}
    context.update(csrf(request))
    return render(request, "post_create.html", context)


def follow(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if not request.user.blog.is_following(blog):
        follow = request.user.blog.follow(blog)
        Activity.create_activity(request.user.blog, follow, FOLLOW)
    return redirect(request.META.get('HTTP_REFERER'))

def unfollow(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.user.blog.is_following(blog):
        follow = Follow.objects.get(follower=request.user.blog, followee=blog)
        follow.delete()
    return redirect(request.META.get('HTTP_REFERER'))

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
    display_info_list=[]
    for post in posts:
        display_info_list.append(PostDisplayInfo(request.user.blog,
                                 post,
                                 Activity.find_activity_for_object(post.pk,
                                                                  ContentType.objects.get_for_model(Post)).activity_type))
    context = {"tag":tag, "display_info_list":display_info_list}
    return render(request, "tagged.html", context)


class ActivityDisplayInfo():

    def __init__(self, current_user_blog, object, activity_type):
        self.activity_type = activity_type
        self.timestamp = object.timestamp

    def is_post(self):
        return self.activity_type == POST

    def is_reblog(self):
        return self.activity_type == REBLOG

    def is_like(self):
        return self.activity_type == LIKE

    def is_follow(self):
        return self.activity_type == FOLLOW

class PostDisplayInfo(ActivityDisplayInfo):

    def __init__(self, current_user_blog, post, activity_type):
        ActivityDisplayInfo.__init__(self, current_user_blog, post, activity_type)
        self.post = post
        self.is_liked = post.is_liked_by(current_user_blog)
        self.reblogs = post.find_notes()
        self.likes = post.find_likes()
        self.tags = post.tags.all()


class BlogDisplayInfo():

    def __init__(self, current_user_blog, blog):
        self.blog = blog
        self.is_followed = current_user_blog.is_following(blog)