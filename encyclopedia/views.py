from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import html

from . import util, forms


def index(request):
    if request.method == 'POST':
        search_field = request.POST.get('search_field')
        all_entries = util.list_entries()
        search_results = []

        for e in all_entries:
            if e.lower() == search_field.lower():
                return HttpResponseRedirect(reverse("entry", args = [search_field]))
            else:
                if search_field.lower() in e.lower():
                    search_results.append(e)

        if len(search_results) != 0:
            return render(request, "encyclopedia/search_results.html", {
                "search_results": search_results,
                "search_field": search_field
            })
        else:
            return HttpResponseRedirect(reverse("entry", args = [search_field]))

    else: 
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def entry(request, entry):
    entryContent = util.github_markup_to_html(util.get_entry(entry))
    if entryContent is None:
        return render(request, "encyclopedia/error.html", {
            "entryName": entry.capitalize(),
            "errorMessage": f"Couldn't find nothing about: {entry} entry" 
        })

    return render(request, "encyclopedia/entry.html", {
        "entryName": entry.capitalize(),
        "entryContent": entryContent,
    })


#adding page -------------
def add_page(request):
    return render(request, "encyclopedia/add_page.html", {
        "entry_form": forms.NewEntryForm()
    })