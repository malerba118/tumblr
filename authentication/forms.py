from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2","email")

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="Username")
    password = forms.CharField(widget=forms.PasswordInput())
