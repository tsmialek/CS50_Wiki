from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import html

from . import util


def index(request):
    if request.method == 'POST':
        search_field = request.POST.get('search_field')

        

        return redirect(reverse("entry", args = [search_field]))
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def entry(request, entry):
    entryContent = util.github_markup_to_html(util.get_entry(entry))
    if entryContent is None:
        return render(request, "encyclopedia/error.html", {
            "entryName": entry.capitalize()
        })

    return render(request, "encyclopedia/entry.html", {
        "entryName": entry.capitalize(),
        "entryContent": entryContent
    })
