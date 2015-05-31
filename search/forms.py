from django import forms


class SearchTagsForm(forms.Form):
    tag = forms.CharField(max_length=50)