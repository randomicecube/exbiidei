from email.policy import default
from django import forms

LIMIT = "Pretende visualizar até quantas publicações?"
OFFSET = "Pretende visualizar a partir de que publicação?"

TITLE = "Qual é o título da publicação?"
AUTHORS = "Quem são os autores?"
ABSTRACT = "Resuma sucintamente a publicação."
LOGO_URL = "Insira um pequeno logotipo para acompanhar a publicação, se assim preferir."
DOC_URL = "Insira um URL para o documento completo, se assim preferir."

class ListAllPapersForm(forms.Form):
  limit = forms.IntegerField(required=False, label=LIMIT)
  offset = forms.IntegerField(required=False, label=OFFSET, initial=1)

class ListSpecificPaperForm(forms.Form):
  paper_id = forms.IntegerField(required=True, label="Paper ID")

class CreatePaperForm(forms.Form):
  title = forms.CharField(max_length=200, required=True, label=TITLE)
  authors = forms.CharField(max_length=200, required=True, label=AUTHORS)
  abstract = forms.CharField(max_length=200, required=True, label=ABSTRACT)
  logoUrl = forms.CharField(max_length=200, required=False, label=LOGO_URL)
  docUrl = forms.CharField(max_length=200, required=False, label=DOC_URL)

class EditPaperForm(forms.Form):
  paper_id = forms.IntegerField(required=True, label="Paper ID")
  title = forms.CharField(max_length=200, required=True, label=TITLE)
  authors = forms.CharField(max_length=200, required=True, label=AUTHORS)
  abstract = forms.CharField(max_length=200, required=True, label="Abstract")
  logoUrl = forms.CharField(max_length=200, required=False, label="Logo URL")
  docUrl = forms.CharField(max_length=200, required=False, label="Doc URL")

class DeletePaperForm(forms.Form):
  paper_id = forms.IntegerField(required=True, label="Paper ID")