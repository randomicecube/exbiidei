from django.shortcuts import render
import requests, os
from .forms import ListAllPapersForm, ListSpecificPaperForm, CreatePaperForm, EditPaperForm, DeletePaperForm

# Create your views here.

PAPERS_ENDPOINT = os.getenv(
  "PAPERS_ENDPOINT",
  default="https://aduck.rnl.tecnico.ulisboa.pt/istpaper/papers"
)

def index(request):
  forms = [ListAllPapersForm(request.GET), ListSpecificPaperForm(request.GET), CreatePaperForm(request.POST), EditPaperForm(request.POST), DeletePaperForm(request.POST)]
  return render(request, "DEIPaper/index.html", {"forms":forms})

def list_all_papers(request):
  """
  Lists all papers.
  Worth noting that we safeguard against a user calling the page directly from its URL
  checking for None, and for them not inputting a limit or offset by checking with isdigit.
  """
  limit = request.GET.get("limit")
  if limit == None or not limit.isdigit():
    limit = 30 # 30 is the default limit chosen
  offset = request.GET.get("offset")
  if offset == None or not offset.isdigit():
    offset = 0 # 0 is the default offset chosen
  print("limit:", limit)
  print("offset:", offset)
  # answer = requests.get(PAPERS_ENDPOINT, params={'limit':limit, 'offset':offset})
  if not limit:
    print("nada")
    # limit = answer.json()['total']
  if not offset:
    offset = 1
  print("Starting to list papers...")
  # print(answer.text)
  print("Done!")
  return render(request, "DEIPaper/list-all-papers.html")

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
  return render(request, "DEIPaper/list-specific-paper.html", {"paper":answer.json()})

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