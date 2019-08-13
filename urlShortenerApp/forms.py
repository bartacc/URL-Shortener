from django import forms

class URLform(forms.Form):
    urlField = forms.URLField(label="Provide a URL to be shortened")