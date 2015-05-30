from django.shortcuts import render

# Create your views here.
from blogging.models import Post
from newsfeed.models import Activity, POST, REBLOG, LIKE


def newsfeed_view(request):
    newsfeed_activities = Activity.find_newsfeed_activities(request.user.blog).order_by("-timestamp")
    activities_w_extra_info = []
    for activity in newsfeed_activities:
        if activity.activity_type == POST or activity.activity_type == REBLOG:
            activities_w_extra_info.append({"activity":activity, "notes": Post.objects.filter(root=activity.object.root)})
        else:
            activities_w_extra_info.append({"activity":activity})
    context = {"activity_dicts":activities_w_extra_info}
    return render(request, "newsfeed.html", context)
