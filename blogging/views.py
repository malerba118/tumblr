import json
from django.contrib import messages
from django.core.context_processors import csrf

from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from blogging.forms import PostCreateForm, BlogEditForm
from blogging.models import Blog, Post, Like, Tag, Activity, POST, REBLOG, FOLLOW, Follow, LIKE
from newsfeed.models import *


def blog_view(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    posts = blog.get_posts()
    post_display_info_list = [PostDisplayInfo(request.user.blog,
                                              post,
                                              Activity.find_activity_for_object(post.pk, ContentType.objects.get_for_model(Post)).activity_type) for post in posts]
    is_following = request.user.blog.is_following(blog)
    has_edit_permissions = blog.isOwnedBy(request.user)
    followers = blog.find_followers()
    follower_info_list = [BlogDisplayInfo(blog, follower) for follower in followers]
    followees = blog.find_followees()
    followee_info_list = [BlogDisplayInfo(blog, followee) for followee in followees]
    context = {"blog":blog,
               "post_display_info_list":post_display_info_list,
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

def blockquotify(blog, post):
    return '<a href="' + blog.get_absolute_url()+ '">' + blog.slug + ": </a>" + "<blockquote>" + post.content+ "</blockquote><hr><p><br></p>"

def reblog_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.root = post.root
            new_post.blog = request.user.blog
            if post.is_root():
                if blockquotify(post.blog, post) == new_post.content:
                    pass
                else:
                    new_post.content = blockquotify(request.user.blog, new_post)
            else:
                if new_post.content != post.content:
                    new_post.content =  blockquotify(request.user.blog, new_post)
            new_post.save()##must persist prior to setting tags field
            new_post.tags = Tag.find_or_create_tags(form.data["tags_field"])
            new_post.save()
            Activity.create_activity(request.user.blog, new_post, REBLOG)
            return redirect(request.user.blog.get_absolute_url())
    form = PostCreateForm()
    form.fields["title"].initial = post.title
    if post.is_root():
        form.fields["content"].initial = blockquotify(post.blog, post)
    else:
        form.fields["content"].initial = post.content
    context = {"post_form": form}
    context.update(csrf(request))
    return render(request, "post_create.html", context)


def post_delete_ajax(request, post_id):
    if  not request.method == "GET":
        return redirect(request.META.get('HTTP_REFERER'))
    post = get_object_or_404(Post, pk=post_id)
    if post.is_owned_by(request.user.blog):
        post.delete()
        is_deleted = Post.objects.filter(pk=post_id).count()==0
        response_dict = {"is_deleted":is_deleted, "post_id":post_id}
        return HttpResponse(json.dumps(response_dict), content_type="application/json")
    return HttpResponseForbidden


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


def like_toggle(request, post_id):
    if not request.method == "POST":
        return redirect(request.META.get('HTTP_REFERER'))
    post = get_object_or_404(Post, pk=post_id)
    if post.is_liked_by(request.user.blog):
        like = get_object_or_404(Like, liker=request.user.blog, liked=post)
        like.delete()
    else:
        like = Like()
        like.liker = request.user.blog
        like.liked = post
        like.save()
    response_dict = {"is_liked":post.is_liked_by(request.user.blog),
                     "post_id":post.pk }
    return HttpResponse(json.dumps(response_dict), content_type='application/json')

def likes_refresh_ajax(request, post_id):
    if not request.method == "GET":
        return redirect(request.META.get('HTTP_REFERER'))
    post = get_object_or_404(Post, pk=post_id)
    likes = post.find_likes()
    likers = []
    for like in likes:
        likers.append({"liker": like.liker.slug, "liker_url": like.liker.get_absolute_url()})
    response_dict = {"likers":likers}
    return HttpResponse(json.dumps(response_dict), content_type='application/json')

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