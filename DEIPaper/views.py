from django.shortcuts import render
import requests, os
from .forms import ListSpecificPaperForm, CreatePaperForm, EditPaperForm, DeletePaperForm
from django.http import HttpRequest

PAPERS_ENDPOINT = os.getenv(
  "PAPERS_ENDPOINT",
  default="https://aduck.rnl.tecnico.ulisboa.pt/istpaper/papers"
)

PAGE_SIZE = 10

def index(request):
  forms = [ListSpecificPaperForm(request.GET), CreatePaperForm(request.POST), EditPaperForm(request.POST), DeletePaperForm(request.POST)]
  return render(request, "DEIPaper/index.html", {"forms":forms})

def list_all_papers(request):
  # TODO: when there isn't a second page, "next" shouldn't be displayed
  """
  Lists all papers.
  """
  first_paper_id = request.GET.get("first_id")
  last_paper_id = request.GET.get("last_id")
  prev_page_clicked = request.GET.get("prev")
  if not first_paper_id or not last_paper_id:
    response = requests.get(PAPERS_ENDPOINT, params={'limit':PAGE_SIZE, 'offset':0})
  else:
    first_paper_id = int(first_paper_id)
    last_paper_id = int(last_paper_id)
    prev_page_clicked = int(prev_page_clicked)
    if not prev_page_clicked:
      response = requests.get(PAPERS_ENDPOINT, params={'limit':PAGE_SIZE, 'offset':last_paper_id})
    else:
      first_paper_id = 0 if first_paper_id <= PAGE_SIZE + 1 else first_paper_id - PAGE_SIZE - 1
      response = requests.get(PAPERS_ENDPOINT, params={'limit':PAGE_SIZE, 'offset':first_paper_id})    
  json = response.json()
  if len(json) == 0: # got to the end of the list
    list_all_papers(HttpRequest())
  return render(request, "DEIPaper/list-all-papers.html", {
    "papers": json,
  })

def list_specific_paper(request):
  """
  Lists a specific paper.
  """
  paper_id = request.GET.get("paper_id")
  if paper_id == None:
    return render(request, "DEIPaper/list-specific-paper.html", {
      "form":ListSpecificPaperForm(request.GET)}
    ) # TODO - ADD ERROR PAGE
  answer = requests.get(PAPERS_ENDPOINT + "/" + paper_id)
  if answer.status_code != 200:
    return render(request, "DEIPaper/list-specific-paper.html", {
      "form":ListSpecificPaperForm(request.GET)}
    )
  print("paper_id:", paper_id)
  print(answer.text)
  return render(request, "DEIPaper/list-specific-paper.html", {
    "paper":answer.json(),
    "form":ListSpecificPaperForm(request.GET)}
  )

def create_paper(request):
  if request.method == "POST":
    print("Gotcha!")
  form = CreatePaperForm(request.POST)
  return render(request, "DEIPaper/create-paper.html", {"forms":[form]})

def edit_paper(request):
  if request.method == "PUT":
    print("Gotcha!")
  form = EditPaperForm(request.PUT)
  return render(request, "DEIPaper/edit-paper.html", {"forms":[form]})

def delete_paper(request):
  if request.method == "DELETE":
    print("Gotcha!")
  form = DeletePaperForm(request.DELETE)
  return render(request, "DEIPaper/delete-paper.html", {"forms":[form]})