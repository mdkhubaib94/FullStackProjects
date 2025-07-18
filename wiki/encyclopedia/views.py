from django.shortcuts import render,redirect

import random

import markdown2 #type:ignore

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    if util.get_entry(title):
       return render(request,"encyclopedia/entry.html",{
            "content" : markdown2.markdown(util.get_entry(title)),
            "title" :title
            })
    else:
        return render(request,"encyclopedia/error.html")
    
def search(request):
    query = request.GET.get("q", "").strip()
    for entry in util.list_entries():

        if entry.lower() == query.lower():
            return redirect("entry", title=query)
        
        elif query.lower() in entry.lower():
            return render(request, "encyclopedia/results.html", {
                "query": query.lower(),
                "entries": util.list_entries()
            })
        
    else:   
       return render(request,"encyclopedia/error.html")
    
def new(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()


        if util.get_entry(title):
            return render(request, "encyclopedia/new.html", {
                "error": "Entry already exists.",
                "title": title,
                "content": content
            })
        
        content = f"# {title}\n\n{content}"
        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/new.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()

        # Normalize line endings: remove repeated blank lines
        lines = content.splitlines()
        cleaned_lines = [line.rstrip() for line in lines]
        cleaned_content = "\n".join(cleaned_lines)

        util.save_entry(title, cleaned_content)
        return redirect("entry", title=title)

    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    if entries:
        selected = random.choice(entries)
        return redirect("entry", title=selected)
