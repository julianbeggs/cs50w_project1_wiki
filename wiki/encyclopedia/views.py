from django.shortcuts import render
from django import forms
from django.urls import reverse
import markdown2
from django.http import HttpResponseRedirect, request, response, QueryDict
from . import util
from django.core.exceptions import ValidationError



def validate_entry_exists(title):
    if util.get_entry(title) != None:
        raise ValidationError(
            "Entry already exists. Check the name or edit existing entry.",
            params={"title": title},
        )

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", validators=[validate_entry_exists])
    entry = forms.CharField(label="Entry", widget=forms.Textarea)
    forms.CharField(widget=forms.Textarea)

def index(request):
    q = request.GET.get('q', None)
    if q == None:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })
    else:
        return entry(request, q)

def entry(request, title):
    q = request.GET.get('q', None)
    if q == None: # no search query param
        if util.get_entry(title) == None:
            entry, title = None
        else:
            entry = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry,
        })
    else: # there is a search query param
        if util.get_entry(q) == None:
            return render(request, "encyclopedia/index.html", {
                "query": q,
                "entries": util.search_results(q),
                })
        else:
            entry = markdown2.markdown(util.get_entry(q))
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title
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
            if util.get_entry(title) == None:
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

