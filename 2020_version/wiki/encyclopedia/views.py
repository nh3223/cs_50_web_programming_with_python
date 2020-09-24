import markdown2
from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from . import util

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Search Encyclopedia',
        'class': 'search'
        }))

def index(request):
    search(request)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title not in util.list_entries():
        return HttpResponse('Entry Not Found')
    return render(request, 'encyclopedia/entry.html', {
        'title': title,
        'content': markdown2.markdown(util.get_entry(title))
    })    

def search(request):
    query = request.GET.get('q')
    if query is not None:
        if query in util.list_entries():
            return render(request, 'encyclopedia/entry.html', {
                    'title': query,
                    'content': markdown2.markdown(util.get_entry(query))
                })  
        entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        return render(request, 'encyclopedia/search_results.html', {
                'entries': entries 
        })

          
