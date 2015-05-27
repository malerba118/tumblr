from django import forms
from blogging.models import Blog


class BlogCreateForm(forms.ModelForm):
    slug = forms.SlugField(label="Desired Blog Url")
    class Meta:
        model = Blog
        fields = ("slug",)

