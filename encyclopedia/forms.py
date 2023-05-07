from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title ", required=True, min_length=1)
    content = forms.CharField(label="Populate your entry with data using GitHub markdown language ",
    required=True, widget=forms.Textarea(attrs={'rows': 5}))