from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView
from django.template.context_processors import csrf
from authentication.forms import UserRegisterForm, UserLoginForm
# Create your views here.
from blogging.forms import BlogCreateForm


def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        blog_form = BlogCreateForm(request.POST)
        if user_form.is_valid() and blog_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.email
            user.save()
            blog = blog_form.save(commit=False)
            blog.user = user
            blog.save()
            return redirect(reverse("log-in"))
    else:
        user_form = UserRegisterForm()
        blog_form = BlogCreateForm()


    context =  {"user_form":user_form, "blog_form":blog_form}
    context.update(csrf(request))

    return render_to_response("register.html",context)


def log_in(request):

    login_form = UserLoginForm(request.POST or None)

    if request.method == "POST":
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
    # the password verified for the user
                if user.is_active:
                    login(request, user)
                    return redirect("newsfeed")
                else:
                    messages.error(request, "This account has been disabled!")
            else:
                messages.error(request, "The username and password were incorrect.", extra_tags="danger")


    context = {"login_form":login_form}
    context.update(csrf(request))
    return render(request, "login.html", context)

def log_out(request):
    logout(request)
    return redirect("log-in")
