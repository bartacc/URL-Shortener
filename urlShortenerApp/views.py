from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from . import forms

# Create your views here.

def index(request):
    context = {}
    if request.method == 'POST':
        form = forms.URLform(request.POST)
        context['form'] = form
        if form.is_valid():
            context['shortened_url'] = form.cleaned_data['urlField']
    else:
        form = forms.URLform()
        context['form'] = form

    return render(request, 'urlShortenerApp/index.html', context)