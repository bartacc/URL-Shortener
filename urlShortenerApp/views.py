from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from shortuuid import uuid

from . import forms
from .models import URL

# Create your views here.

def index(request):
    context = {}
    #If POST then take input from form, and consult the database for a given URL (either return an already exisiting shortened URL from database or create a new one and save to database)
    if request.method == 'POST':
        form = forms.URLform(request.POST)
        context['form'] = form
        if form.is_valid():
            provided_url = form.cleaned_data['urlField']
            url_in_database = _find_url_in_database(url=provided_url)
            if(url_in_database is None):
                shortened_url = uuid(name=provided_url)[:10]
                new_url_in_database = URL(url=provided_url, hashed_url=shortened_url)
                new_url_in_database.save()
            else:
                shortened_url = url_in_database.hashed_url

            context['shortened_url'] = shortened_url
    #If GET then create a new, empty form
    else:
        form = forms.URLform()
        context['form'] = form

    return render(request, 'urlShortenerApp/index.html', context)


def redirect_to_url(request, shortened_url):
    url_in_database = _find_url_in_database(shortened_url=shortened_url)
    if(url_in_database is None):
        return redirect('index')
    else:
        original_url = url_in_database.url
        return redirect(original_url)
    
"Return URL model object from database or None if non-existent. Provide either url or shortened_url to be searched"
def _find_url_in_database(url='', shortened_url=''):
    url_in_database = None
    try:
        if url:
            url_in_database = URL.objects.get(url=url)
            print("Searching for URL in database: " + url)
        elif shortened_url:
            url_in_database = URL.objects.get(hashed_url=shortened_url)
            print("Searching for URL in database: " + shortened_url)
    except ObjectDoesNotExist:
        url_in_database = None
    finally:
        return url_in_database