import markdown2

from django.http import HttpResponse
from django.shortcuts import render


from . import util


def index(request):
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

