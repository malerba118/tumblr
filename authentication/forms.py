from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")