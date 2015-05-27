from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.template.context_processors import csrf
from authentication.forms import UserForm
# Create your views here.



def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.email
            user.save()
            return HttpResponseRedirect("home")
    else:
        user_form = UserForm()

    c =  {"user_form":user_form}
    c.update(csrf(request))

    return render_to_response("register.html",c)

