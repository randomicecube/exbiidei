from django.shortcuts import render
import requests, os
from .forms import ListSpecificPaperForm, CreatePaperForm, EditPaperForm, DeletePaperForm
from django.http import HttpRequest

ISTPAPER_ENDPOINT = os.getenv(
  "ISTPAPER_ENDPOINT",
  default="https://aduck.rnl.tecnico.ulisboa.pt/istpaper/papers"
)

AUTH_TOKEN = os.getenv("AUTH_TOKEN")

PAGE_SIZE = 10

def index(request):
  """
  Renders the homepage.
  """
  return render(request, "DEIPaper/index.html", {
    "forms": [
      ListSpecificPaperForm(),
      CreatePaperForm(),
    ]
  })

def list_all_papers(request):
  """
  Renders the page with a listing of all the papers stored in the database.
  """
  prev_page_clicked = request.GET.get("prev")
  page = int(request.GET.get("page", "0"))

  # prev_page_button/next_page_button:
  # represent whether in the rendered page, we have to display the prev/next page button
  prev_page_button = False
  next_page_button = False

  # note: we consider limit as PAGE_SIZE + 1 so we can check if there's a next page
  limit = PAGE_SIZE + 1

  if page == 0:
    offset = 0
    page += 1
  else:
    prev_page_clicked = int(prev_page_clicked)
    if not prev_page_clicked:
      page += 1
      offset = max(PAGE_SIZE * (page - 1), 0)
      if offset > 0:
        prev_page_button = True
    else:
      page -= 1
      offset = max(PAGE_SIZE * (page - 1 - 1), 0)
      if offset > 0:
        prev_page_button = True

  response = requests.get(ISTPAPER_ENDPOINT, params={
    'limit': limit,
    'offset': offset,
  })
  json = response.json()

  if len(json) == 0: # got to the end of the list
    return list_all_papers(HttpRequest())
  elif len(json) > PAGE_SIZE: # there is a next page
    json = json[:-1] # the last element would be in the next page
    next_page_button = True
  
  return render(request, "DEIPaper/list-all-papers.html", {
    "papers": json,
    "prev_page": prev_page_button,
    "next_page": next_page_button,
    "form": DeletePaperForm(),
    "status_code": response.status_code,
    "page": page,
  })

def list_specific_paper(request):
  """
  Renders the page which lists detailed information about a specific paper.
  """
  paper_id = request.GET.get("id")
  if not paper_id: # user accessed the URL directly, not filling a form
    return render(request, "DEIPaper/list-specific-paper.html", {
      "form": ListSpecificPaperForm(),
      "direct_access": True,
    })
  
  response = requests.get(ISTPAPER_ENDPOINT + "/" + paper_id)
  if response.status_code != 200:
    return render(request, "DEIPaper/list-specific-paper.html", {
      "status_code": response.status_code,
    })
  
  return render(request, "DEIPaper/list-specific-paper.html", {
    "response": response.json(),
    "status_code": response.status_code,
    "forms": [
      ListSpecificPaperForm(),
      EditPaperForm(initial=response.json()),
      DeletePaperForm(),
    ]
  })

def create_paper(request):
  """
  Renders the page which allows the user to create a new paper.
  """
  title = request.POST.get("title")
  authors = request.POST.get("authors")
  abstract = request.POST.get("abstract")
  logoUrl = request.POST.get("logoUrl", "")
  docUrl = request.POST.get("docUrl", "")
  if not title: # user accessed the URL directly, not filling a form
    return render(request, "DEIPaper/create-paper.html", {
      "form": CreatePaperForm(),
      "direct_access": True,
    })
  response = requests.post(ISTPAPER_ENDPOINT, json={
    "title": title,
    "authors": authors,
    "abstract": abstract,
    "logoUrl": logoUrl,
    "docUrl": docUrl
  }, headers={
    "Authorization": "Bearer " + AUTH_TOKEN
  })

  if response.status_code != 201:
    return render(request, "DEIPaper/create-paper.html", {
      "status_code": response.status_code,
      "form": CreatePaperForm(),
    })

  return render(request, "DEIPaper/create-paper.html", {
    "response": response.json(),
    "status_code": response.status_code,
    "form": CreatePaperForm(),
  })

def edit_paper(request):
  """
  Renders the page shown after a user edits a paper.
  """
  paper_id = request.POST.get("id", "")
  title = request.POST.get("title", "")
  authors = request.POST.get("authors", "")
  abstract = request.POST.get("abstract", "")
  logoUrl = request.POST.get("logoUrl", "")
  docUrl = request.POST.get("docUrl", "")
  if not paper_id: # user accessed the URL directly, not filling a form
    return render(request, "DEIPaper/edit-paper.html", {
      "form": EditPaperForm(request.GET),
      "direct_access": True
    })
  
  response = requests.put(ISTPAPER_ENDPOINT + "/" + paper_id, json={
    "title": title,
    "authors": authors,
    "abstract": abstract,
    "logoUrl": logoUrl,
    "docUrl": docUrl
  }, headers={
    "Authorization": "Bearer " + AUTH_TOKEN
  })

  if response.status_code != 200:
    return render(request, "DEIPaper/edit-paper.html", {
      "status_code": response.status_code,
      "form": EditPaperForm(request.GET),
    })

  return render(request, "DEIPaper/edit-paper.html", {
    "response": response.json(),
    "status_code": response.status_code,
    "form": EditPaperForm()}
  )

def delete_paper(request):
  """
  Renders the page shown after a user deletes a paper.
  """
  paper_id = request.GET.get("id")
  if not paper_id:
    return render(request, "DEIPaper/delete-paper.html", {
      "form": DeletePaperForm(),
      "direct_access": True,
    })
  
  response = requests.delete(ISTPAPER_ENDPOINT + "/" + paper_id, headers={
    "Authorization": "Bearer " + AUTH_TOKEN
  })

  return render(request, "DEIPaper/delete-paper.html", {
    "status_code": response.status_code,
    "form": DeletePaperForm()
  })
    