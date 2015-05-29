from django.shortcuts import render

# Create your views here.
from newsfeed.models import Activity


def newsfeed_view(request):
    newsfeed_activities = Activity.find_newsfeed_activities(request.user.blog).order_by("-timestamp")
    context = {"activities":newsfeed_activities}
    return render(request, "newsfeed.html", context)
