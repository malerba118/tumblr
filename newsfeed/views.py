import json
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import Template, loader
from blogging.models import Post, Like
from blogging.models import Activity, POST, REBLOG, LIKE
from blogging.views import PostDisplayInfo


def newsfeed_view(request):
    newsfeed_activities = Activity.find_newsfeed_activities(request.user.blog).order_by("-timestamp")
    display_info_list=[]
    for activity in newsfeed_activities:
        if activity.activity_type == POST or activity.activity_type == REBLOG:
            display_info_list.append(PostDisplayInfo(request.user.blog, activity.object, activity.activity_type))

    #context = {"activity_dicts":activities_w_extra_info}
    context = {"display_info_list":display_info_list}
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

def load_more_posts(request):
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