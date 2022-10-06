from django import forms
from django.forms import TextInput


class SearchForm(forms.Form):
    title = forms.CharField(max_length=50)
    widgets = {'title': TextInput(attrs={'class': 'input', 'placeholder': 'Title of video'})}
