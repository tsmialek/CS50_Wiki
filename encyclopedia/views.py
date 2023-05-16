from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from fuzzywuzzy import fuzz
import html
import random
import io, os
from django import forms
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
                if fuzz.ratio(e.lower(), search_field.lower()) > 50:
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
            "errorMessage": f"Couldn't find nothing about: {entry} entry" 
        })

    return render(request, "encyclopedia/entry.html", {
        "entryName": entry.capitalize(),
        "entryContent": entryContent,
    })


#adding page -------------
def add_page(request):
    if request.method == 'POST':
        form = forms.NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if not os.path.exists(f'entries/{title.capitalize()}.md'):
                with io.open(f'entries/{title}.md', 'w', encoding='utf-8') as entry:
                    entry.write(content)
            else: 
                return render(request, "encyclopedia/error.html", {
                    'errorMessage': f'Entry with this title already exists'
                })
    return render(request, "encyclopedia/add_page.html", {
        "entry_form": forms.NewEntryForm(),
        "action": "Add"
    })

def edit_page(request, entry):
    if request.method == 'POST':
        form = forms.NewEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            with io.open(f'entries/{entry}.md', 'w', encoding='utf-8') as entryFile:
                entryFile.write(content)
            
            return HttpResponseRedirect(reverse("entry", args = [entry]))
        else:
            return render(request, 'encyclopedia/error.html', {
                'errorMessage': f'Unable to modify that entry. Make sure you provided correct input'
            })

    form = forms.NewEntryForm(initial={'title': entry, 'content': util.get_entry(entry)})
    form.fields['title'].widget.attrs['readonly'] = True
    return render(request, "encyclopedia/add_page.html", {
        'entry_form': form,
        'action': 'Edit',
        'entry' : entry
    })

def random_page(request):
    list_of_entries = util.list_entries()
    return HttpResponseRedirect(reverse("entry", args = [random.choice(list_of_entries)]))