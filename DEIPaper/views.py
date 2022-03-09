from django.shortcuts import render
import requests, os
from .forms import ListSpecificPaperForm, CreatePaperForm, EditPaperForm, DeletePaperForm
from django.http import HttpRequest

PAPERS_ENDPOINT = os.getenv(
  "PAPERS_ENDPOINT",
  default="https://aduck.rnl.tecnico.ulisboa.pt/istpaper/papers"
)

AUTHENTICATION_TOKEN = os.getenv(
  "AUTHENTICATION_TOKEN",
  default="ist199207"
)

PAGE_SIZE = 10

def index(request):
  return render(request, "DEIPaper/index.html", 
    {"forms":[
      ListSpecificPaperForm(request.GET),
      CreatePaperForm(request.POST),
    ]}
  )

def list_all_papers(request):
  """
  Lists all papers.
  IMPORTANT NOTE: we always request PAGE_SIZE+1 papers, so that we can check if there is a next page to be displayed or not.
  """
  first_paper_id = request.GET.get("first_id")
  last_paper_id = request.GET.get("last_id")
  prev_page_clicked = request.GET.get("prev")
  if not first_paper_id:
    prev_page = False
    response = requests.get(PAPERS_ENDPOINT, params={'limit':PAGE_SIZE + 1, 'offset':0})
  else:
    first_paper_id = int(first_paper_id)
    last_paper_id = int(last_paper_id)
    prev_page_clicked = int(prev_page_clicked)
    if not prev_page_clicked:
      prev_page = True
      response = requests.get(PAPERS_ENDPOINT, params={'limit':PAGE_SIZE + 1, 'offset':last_paper_id})
    else:
      first_paper_id = 0 if first_paper_id <= PAGE_SIZE + 1 else first_paper_id - PAGE_SIZE - 1
      prev_page = (first_paper_id != 0)
      response = requests.get(PAPERS_ENDPOINT, params={'limit':PAGE_SIZE + 1, 'offset':first_paper_id})    
  
  json = response.json()
  next_page = (len(json) > PAGE_SIZE)
  if len(json) == 0: # got to the end of the list
    return list_all_papers(HttpRequest())
  elif len(json) > 10:
    json = json[:-1]
  print("prev_page: " + str(prev_page))
  print("next_page: " + str(next_page))
  return render(request, "DEIPaper/list-all-papers.html", {
    "papers": json, # the last element would be in the next page
    "prev_page": prev_page,
    "next_page": next_page,
    "form": DeletePaperForm(),
    "status_code": response.status_code,
  })

def list_specific_paper(request):
  """
  Lists a specific paper.
  """
  paper_id = request.GET.get("id")
  if not paper_id:
    return render(request, "DEIPaper/list-specific-paper.html", {
      "form":ListSpecificPaperForm()}
    )
  response = requests.get(PAPERS_ENDPOINT + "/" + paper_id)
  # print debug
  print(response.json())
  print("response'status code is " + str(response.status_code))
  return render(request, "DEIPaper/list-specific-paper.html", {
    "response":response.json(),
    "status_code":response.status_code,
    "forms":[
      ListSpecificPaperForm(),
      EditPaperForm(initial=response.json()),
      DeletePaperForm()
    ]}
  )

def create_paper(request):
  title = request.POST.get("title")
  authors = request.POST.get("authors")
  abstract = request.POST.get("abstract")
  logoUrl = request.POST.get("logoUrl", "")
  docUrl = request.POST.get("docUrl", "")
  print(title, authors, abstract, logoUrl, docUrl)
  if not title: #user accessed the URL directly, not filling a form
    return render(request, "DEIPaper/create-paper.html", {
      "form":CreatePaperForm()}
    )
  # TODO - CLEANED DATA
  response = requests.post(PAPERS_ENDPOINT, json={
    "title":title,
    "authors":authors,
    "abstract":abstract,
    "logoUrl":logoUrl,
    "docUrl":docUrl
  }, headers={
    "Authorization": "Bearer " + AUTHENTICATION_TOKEN
  })
  # if the paper was created successfully, redirect to a new page which:
  # - can redirect to the homepage
  # - can redirect to the specific paper view
  # error page with option to create a new paper or homepage
  return render(request, "DEIPaper/create-paper.html", {
    "response":response.json(),
    "status_code":response.status_code,
    "form":CreatePaperForm()}
  )

def edit_paper(request):
  paper_id = request.POST.get("id", "")
  title = request.POST.get("title", "")
  authors = request.POST.get("authors", "")
  abstract = request.POST.get("abstract", "")
  logoUrl = request.POST.get("logoUrl", "")
  docUrl = request.POST.get("docUrl", "")
  print("--------\n" + paper_id, title, authors, abstract, logoUrl, docUrl + "\n--------\n")
  if not paper_id:
    print("paper_id is None")
    return render(request, "DEIPaper/edit-paper.html", {
      "form":EditPaperForm(request.GET),
    })
  print("Paper ID is " + paper_id)
  response = requests.put(PAPERS_ENDPOINT + "/" + paper_id, json={
    "title":title,
    "authors":authors,
    "abstract":abstract,
    "logoUrl":logoUrl,
    "docUrl":docUrl
  }, headers={
    "Authorization": "Bearer " + AUTHENTICATION_TOKEN
  })
  return render(request, "DEIPaper/edit-paper.html", {
    "response":response.json(),
    "status_code":response.status_code,
    "form":EditPaperForm()}
  )

def delete_paper(request):
  paper_id = request.GET.get("id")
  if not paper_id:
    return render(request, "DEIPaper/delete-paper.html", {
      "form":DeletePaperForm()}
    )
  response = requests.delete(PAPERS_ENDPOINT + "/" + paper_id, headers={
    "Authorization": "Bearer " + AUTHENTICATION_TOKEN
  })
  return render(request, "DEIPaper/delete-paper.html", {
    "response":response.json(),
    "status_code":response.status_code,
    "form":DeletePaperForm()}
  )
    