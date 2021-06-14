from django.shortcuts import render
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
	
def readEntry(request, entryName):

    text = util.get_entry(entryName)

    if text == None:                            # not found
        text = "<h1>Page was not found</h1>"
        return render(request, "encyclopedia/message.html", {
            "a": text
    })

    else:
        text = markdown2.markdown(text)         # from markdown to html

    return render(request, "encyclopedia/entry.html", {     # view entry
        "a" : text,
        "entryName" : entryName
    })

def searchEntry(request):

    searchName = request.POST.get('q')
    entries = util.list_entries()
    found = []                                              # list of possible entries

    if searchName in entries:                               # entry was found
        text = util.get_entry(searchName)
        text = markdown2.markdown(text)

        return render(request, "encyclopedia/entry.html", {
            "a" : text,
            "entryName": searchName
        })

    for entry in entries:                                   # find letters at beginnig of entryname
        b = entry.find(searchName)
        if b == 0:
            found.append(entry)

    if len(found) == 0:                                     # not found in entries list
        text = "<h1>Entry was not found</h1>"
        return render(request, "encyclopedia/message.html", {
            "a" : text
        })

    return render(request, "encyclopedia/index.html", {     # send answer
        "entries" : found
    })

def newPage(request):

    if request.method == "POST":                            # get data from form
        newTitle = request.POST.get('nTitle')
        newContent = request.POST.get('nContent')

        if newTitle == "" or newContent == "":              # one of fields in form is empty
            text = "<h1>Empty field</h1>"
            return render(request, "encyclopedia/message.html", {
                "a": text
            })

        entries = util.list_entries()
        if newTitle in entries:                             # entry already exists
            text = "<h1>Enter already exists</h1>"
            return render(request, "encyclopedia/message.html", {
                "a": text
            })

        util.save_entry(newTitle, newContent)               # create new entry

        return render(request, "encyclopedia/entry.html", {     # view new entry
            "a": markdown2.markdown(util.get_entry(newTitle)),
            "entryName": newTitle
        })

    return render(request, "encyclopedia/newPage.html")


def editPage(request, entryName):

    if request.method == "POST":                            # get data from form

        newContent = request.POST.get('nContent')
        util.save_entry(entryName, newContent)              # save new content

        return render(request, "encyclopedia/entry.html", {     # view entry with new content
            "a": markdown2.markdown(util.get_entry(entryName)),
            "entryName": entryName
        })

    return render(request, "encyclopedia/editPage.html", {      # view edit form for entry
        "entryName" : entryName,
        "a": util.get_entry(entryName)
    })

def randomPage(request):

    entries = util.list_entries()
    l = len(entries)
    a = random.randrange(l)                             # entry index, min = 0 , max = number of etries - 1
    text = util.get_entry(entries[a])
    text = markdown2.markdown(text)
    return render(request, "encyclopedia/entry.html", {
        "a" : text,
        "entryName": entries[a]
    })
