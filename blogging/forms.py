from django import forms
from blogging.models import Blog, Post


class BlogCreateForm(forms.ModelForm):
    slug = forms.SlugField(label="Desired Blog Url")
    class Meta:
        model = Blog
        fields = ("slug",)


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content",)
