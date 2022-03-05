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
  # limit = int(request.GET.get("limit", default=40))
  # offset = int(request.GET.get("offset", default=1))
  # print("limit:", limit)
  # print("offset:", offset)
  # answer = requests.get(PAPERS_ENDPOINT, params={'limit':limit, 'offset':offset})
  # if not limit:
  #   limit = answer.json()['total']
  # if not offset:
  #   offset = 1
  # print("Starting to list papers...")
  # print(answer.text)
  # print("Done!")
  if request.method == "GET":
    print("Gotcha!")
  form = ListAllPapersForm(request.GET)
  return render(request, "DEIPaper/index.html")

def list_specific_paper(request):
  if request.method == "GET":
    print("Gotcha!")
  form = ListSpecificPaperForm(request.GET)
  return render(request, "DEIPaper/index.html", {"forms":[form]})

def create_paper(request):
  if request.method == "POST":
    print("Gotcha!")
  form = CreatePaperForm(request.POST)
  return render(request, "DEIPaper/index.html", {"forms":[form]})

def edit_paper(request):
  if request.method == "POST":
    print("Gotcha!")
  form = EditPaperForm(request.POST)
  return render(request, "DEIPaper/index.html", {"forms":[form]})

def delete_paper(request):
  if request.method == "POST":
    print("Gotcha!")
  form = DeletePaperForm(request.POST)
  return render(request, "DEIPaper/index.html", {"forms":[form]})