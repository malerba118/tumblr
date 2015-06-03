from django.core.context_processors import csrf
from django.shortcuts import render

# Create your views here.
from blogging.models import Post, Like
from blogging.models import Activity, POST, REBLOG, LIKE
from blogging.views import PostDisplayInfo


def newsfeed_view(request):
    newsfeed_activities = Activity.find_newsfeed_activities(request.user.blog).order_by("-timestamp")
    activities_w_extra_info = []
    display_info_list=[]
    for activity in newsfeed_activities:
        if activity.activity_type == POST or activity.activity_type == REBLOG:
            display_info_list.append(PostDisplayInfo(request.user.blog, activity.object, activity.activity_type))
            activities_w_extra_info.append({"activity":activity,
                                            "reblogs": activity.object.find_notes(),
                                            "likes": activity.object.find_likes(),
                                            "is_liked": activity.object.is_liked_by(request.user.blog),
                                            "tags": activity.object.tags.all()})
        else:
            activities_w_extra_info.append({"activity":activity})
    #context = {"activity_dicts":activities_w_extra_info}
    context = {"display_info_list":display_info_list}
    context.update(csrf(request))
    return render(request, "newsfeed.html", context)
