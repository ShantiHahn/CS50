from django.shortcuts import render
from django import forms

from . import util
#imports
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import random
import re
import markdown2

##class form
class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="New entry title")
    entry_content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}),label="New entry content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


##testing the entry page
def get_page(request, title):
    content = util.get_entry(title)
    if content is not None :
        content_html = markdown2.markdown(content)
        return render(request, "encyclopedia/title.html", {
            "content": content_html,
            "title": title
    })
    else :
        return render(request, "encyclopedia/error.html", {
            "title": title
        
    })

###modify entry wiki

def edit_content(request, title):

    entry_title = title
    entry_content = util.get_entry(title)
    form = NewEntryForm(initial={'entry_title':entry_title, 'entry_content':entry_content})
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"]
            entry_content = form.cleaned_data["entry_content"]
            util.save_entry(entry_title, entry_content)
            return get_page(request, entry_title)
    return render(request, "encyclopedia/edit_page.html", {
        "title" : title,
        "form": form
    })


### add entry to wiki
def new_page(request):

    if request.method == "POST":

        form = NewEntryForm(request.POST)

        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"]
            entry_content = form.cleaned_data["entry_content"]
            if util.get_entry(entry_title) is None:
                util.save_entry(entry_title,entry_content)
                return get_page(request, entry_title)
            else:
                return render(request, "encyclopedia/new_page.html", {
                    "form": NewEntryForm(initial={"entry_title":entry_title, "entry_content": entry_content}),
                    "title": entry_title,
                    "error_msg": "Error this entry already exists, please go to the links below:"
                })
    return render(request, "encyclopedia/new_page.html", {
        "form":NewEntryForm()
    })


##not exactly what i want
def random_page(request):
    entries_list = util.list_entries()
    stop = len(entries_list)
    random_entry = random.randrange(stop)
    title = entries_list[random_entry]
    content = util.get_entry(title)
    content_html = markdown2.markdown(content)
    return render(request, "encyclopedia/title.html", {
            "content": content_html,
            "title": title
    })



##### basic search

def search_page(request):
    entries_list = util.list_entries()
    search_list = []
    ##search string that comes from the html form
    pattern = request.POST.get("search_page")
    for i in range(len(entries_list)):
        a = re.match(pattern.lower(),entries_list[i].lower())
        if a is not None :
            search_list.append(entries_list[i])
    if search_list == []:
        return render(request, "encyclopedia/error.html", {
            "title": pattern
        } )

    return render(request, "encyclopedia/search_page.html", {
        "entries": search_list
    })
