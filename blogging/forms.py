from fileinput import FileInput
import re
from django import forms
from django.forms import ClearableFileInput
from blogging.models import Blog, Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget




class BlogCreateForm(forms.ModelForm):
    slug = forms.SlugField(label="Desired Blog Url")
    class Meta:
        model = Blog
        fields = ("slug",)

class BlogEditForm(forms.ModelForm):
    #image = forms.ImageField()
    class Meta:
        model = Blog
        fields = ("slug", "title", "description", "template", "image")
        widgets = {
            "image" : ClearableFileInput,
        }

class PostCreateForm(forms.ModelForm):
    tags_field = forms.CharField(max_length=200, required=False)
    class Meta:
        model = Post
        fields = ("title", "content",)
        widgets = {
            'content': SummernoteWidget(),
        }


