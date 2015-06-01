import re
from django import forms
from blogging.models import Blog, Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget




class BlogCreateForm(forms.ModelForm):
    slug = forms.SlugField(label="Desired Blog Url")
    class Meta:
        model = Blog
        fields = ("slug",)

class BlogEditForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ("slug", "title", "description", "template")

class PostCreateForm(forms.ModelForm):
    tags_field = forms.CharField(max_length=200, required=False)
    class Meta:
        model = Post
        fields = ("title", "content",)
        widgets = {
            'content': SummernoteWidget(),
        }


