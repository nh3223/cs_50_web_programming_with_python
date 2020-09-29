import markdown2
import os
import random
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Insert Content Here'}))

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Insert Content Here'}))

def index(request):
    search(request)
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def entry(request, title):
    if title not in util.list_entries():
        return HttpResponse('Entry Not Found')
    return render(request, 'encyclopedia/entry.html', {'title': title, 'content': markdown2.markdown(util.get_entry(title))})    

def search(request):
    query = request.GET.get('q')
    if query is not None:
        if query in util.list_entries():
            return render(request, 'encyclopedia/entry.html', {'title': query, 'content': markdown2.markdown(util.get_entry(query))})  
        
        entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        return render(request, 'encyclopedia/search_results.html', {'entries': entries})

def new_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                return HttpResponse('Duplicate Entry')
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('encyclopedia:entry', title=title)
        
        else:
            return render(request, "encyclopedia/new_page.html", {"form": form})

    else:
        return render(request, "encyclopedia/new_page.html", {"form": NewEntryForm()})

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST, {'content': util.get_entry(title)})
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('encyclopedia:entry', title=title)
        
        else:
            return render(request, "encyclopedia/edit.html", {"form": form})

    else:
        return render(request, "encyclopedia/edit.html", {'title': title, "form": EditForm({'content': util.get_entry(title)})})    

def random_page(request):
    title = random.choice([entry for entry in util.list_entries()])
    return render(request, "encyclopedia/entry.html", {'title': title, 'content': markdown2.markdown(util.get_entry(title))})