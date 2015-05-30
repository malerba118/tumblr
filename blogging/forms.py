import re
from django import forms
from blogging.models import Blog, Post


class BlogCreateForm(forms.ModelForm):
    slug = forms.SlugField(label="Desired Blog Url")
    class Meta:
        model = Blog
        fields = ("slug",)


class PostCreateForm(forms.ModelForm):
    tags_field = forms.CharField(max_length=200)
    class Meta:
        model = Post
        fields = ("title", "content",)

