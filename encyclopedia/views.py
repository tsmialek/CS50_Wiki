from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    entryContent = util.get_entry(entry)

    return render(request, "encyclopedia/entry.html", {
        "entryName": entry,
        "entryContent": entryContent
    })
