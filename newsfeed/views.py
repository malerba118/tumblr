from django.core.context_processors import csrf
from django.shortcuts import render

# Create your views here.
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
