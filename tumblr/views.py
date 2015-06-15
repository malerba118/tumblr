from django.views.generic import TemplateView
from django.shortcuts import redirect

def home(request):
    return redirect("newsfeed")

