from django.shortcuts import render
import markdown2
from django.http import request, response, QueryDict
from . import util


def index(request):
    filter = request.GET.get('q', None)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(filter),
        "filter": filter
    })

def entry(request, title):
    filter = request.GET.get('q', None)
    if filter:
        title = filter
    if util.get_entry(title) != None:
        entry = markdown2.markdown(util.get_entry(title))
    else:
        entry = None
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry,
    })

def new(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def edit(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def random(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

