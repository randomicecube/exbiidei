from django import forms

TITLE = "Qual é o título da publicação?"
AUTHORS = "Quem são os autores da publicação?"
ABSTRACT = "Resuma sucintamente a publicação que pretende adicionar."
LOGO_URL = "Insira um pequeno logotipo para acompanhar a publicação, se assim preferir."
DOC_URL = "Insira um URL para o documento completo, se assim preferir."

class ListSpecificPaperForm(forms.Form):
  id = forms.IntegerField(required=True, label="Paper ID")

class CreatePaperForm(forms.Form):
  title = forms.CharField(max_length=200, required=True, label=TITLE)
  authors = forms.CharField(max_length=500, required=True, label=AUTHORS)
  abstract = forms.CharField(max_length=2000, required=True, label=ABSTRACT)
  logoUrl = forms.CharField(max_length=2000, required=False, label=LOGO_URL)
  docUrl = forms.CharField(max_length=2000, required=False, label=DOC_URL)

class EditPaperForm(forms.Form):
  id = forms.IntegerField(required=True, label="Paper ID")
  title = forms.CharField(max_length=200, required=False, label="Se pretender alterar o título, insira-o aqui.")
  authors = forms.CharField(max_length=500, required=False, label="Se pretender alterar os autores, insira-os aqui.")
  abstract = forms.CharField(max_length=2000, required=False, label="Se pretender alterar o resumo, insira-o aqui.")
  logoUrl = forms.CharField(max_length=2000, required=False, label="Se pretender alterar/adicionar o logotipo, insira-o aqui.")
  docUrl = forms.CharField(max_length=2000, required=False, label="Se pretender alterar/adicionar o documento, insira-o aqui.")

  # setting id as readonly - "disabled" does not work, since it is not returned from the template
  def __init__(self, *args, **kwargs):
    super(EditPaperForm, self).__init__(*args, **kwargs)
    self.fields['id'].widget.attrs['readonly'] = True

class DeletePaperForm(forms.Form):
  id = forms.IntegerField(required=True, label="Paper ID")