from django.shortcuts import render
from django import forms
from django.urls import reverse
import markdown2
from django.http import HttpResponseRedirect, request, response, QueryDict
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    entry = forms.CharField(label="Entry", widget=forms.Textarea)
    forms.CharField(widget=forms.Textarea)

def index(request):
    query = request.GET.get('q', None)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(query),
        "query": query
    })

def entry(request, title):
    filter = request.GET.get('q', None)
    if filter != None:
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
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the entry from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]
            
            # Save the new entry to file
            util.save_entry(title, entry)
            
            # Redirect user to entry
            request.method = "GET"
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title": title}))

        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

    # Request.method is GET
    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })

def edit(request, title):
    if util.get_entry(title) != None:
        entry = markdown2.markdown(util.get_entry(title))
    else:
        entry = None
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry": entry,
    })
    
def random(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

