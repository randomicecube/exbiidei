from django.shortcuts import render

# Create your views here.

def index(request):
  return render(request, "DEIPaper/base.html", {}) # TODO - change this to index.html