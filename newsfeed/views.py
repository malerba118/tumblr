import json
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import Template, loader
from blogging.models import Post, Like
from blogging.models import Activity, POST, REBLOG, LIKE
from blogging.views import PostDisplayInfo

@login_required(login_url='/auth/login/')
def newsfeed_view(request):
    """
    Render view for logged in user's newsfeed
    :param request: http request
    :return: rendered newsfeed template
    """
    context = {}
    context.update(csrf(request))
    return render(request, "newsfeed.html", context)

# def load_more_posts(request):
#     if not request.method == "GET":
#         return redirect(request.META.get('HTTP_REFERER'))
#     offset = int(request.GET["offset"])
#     newsfeed_activities = Activity.find_newsfeed_activities(request.user.blog).order_by("-timestamp")[offset:offset+NUM_NEW_POSTS_TO_LOAD]
#     display_info_list=[]
#     for activity in newsfeed_activities:
#         if activity.activity_type == POST or activity.activity_type == REBLOG:
#             display_info_list.append(PostDisplayInfo(request.user.blog, activity.object, activity.activity_type).as_dict())
#     response_dict = {"posts": display_info_list}
#     return HttpResponse(json.dumps(response_dict), content_type='application/json')

@login_required(login_url='/auth/login/')
def load_more_newsfeed_posts(request):
    """
    Asynchronously load NUM_POSTS_TO_LOAD more posts onto the client's newsfeed.
    Posts are rendered server side and html is passed back to client.
    offset : num posts already loaded onto newsfeed
    NUM_POSTS_TO_RETRIEVE : num posts to render and send back to client
    """
    if not request.method == "GET":
        return redirect(request.META.get('HTTP_REFERER'))
    offset = int(request.GET["offset"])
    NUM_POSTS_TO_LOAD = int(request.GET["NUM_POSTS_TO_RETRIEVE"])
    newsfeed_activities = Activity.find_newsfeed_activities(request.user.blog).order_by("-timestamp")[offset:offset+NUM_POSTS_TO_LOAD]
    display_info_list=[]
    for activity in newsfeed_activities:
        if activity.activity_type == POST or activity.activity_type == REBLOG:
            display_info_list.append(PostDisplayInfo(request.user.blog, activity.object, activity.activity_type))
    context = {"display_info_list": display_info_list}
    raw_template = loader.get_template("posts.html")
    rendered_template = raw_template.render(context)
    return HttpResponse(rendered_template, content_type='text/html')