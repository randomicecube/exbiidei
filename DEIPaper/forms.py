from django import forms

# Form text macros - done this was so they can be easily changed and/or translated
CREATE_TITLE = "Qual é o título da publicação?"
CREATE_AUTHORS = "Quem são os autores da publicação?"
CREATE_ABSTRACT = "Resuma sucintamente a publicação que pretende adicionar."
CREATE_LOGO_URL = "Insira um pequeno logotipo para acompanhar a publicação, se assim preferir."
CREATE_DOC_URL = "Insira um URL para o documento completo, se assim preferir."

EDIT_TITLE = "Se pretender alterar o título, altere-o aqui."
EDIT_AUTHORS = "Se pretender alterar os autores, altere-os aqui."
EDIT_ABSTRACT = "Se pretender alterar a secção de resumo, altere-a aqui."
EDIT_LOGO_URL = "Se pretender alterar/adicionar o logotipo, altere-o aqui."
EDIT_DOC_URL = "Se pretender alterar/adicionar o documento, altere-o aqui."

# Macros for lengths - easier to edit them this way
LENGTH_TITLE = 200
LENGTH_AUTHORS = 500
LENGTH_ABSTRACT = 5000
LENGTH_LOGO_URL = 3000
LENGTH_DOC_URL = 3000

# Form used for searching for a specific paper
class ListSpecificPaperForm(forms.Form):
  id = forms.IntegerField(required=True, label="Paper ID")

# Form used for creating a new paper
class CreatePaperForm(forms.Form):
  title = forms.CharField(max_length=LENGTH_TITLE, required=True, label=CREATE_TITLE)
  authors = forms.CharField(max_length=LENGTH_AUTHORS, required=True, label=CREATE_AUTHORS)
  abstract = forms.CharField(max_length=LENGTH_ABSTRACT, required=True, label=CREATE_ABSTRACT)
  logoUrl = forms.CharField(max_length=LENGTH_LOGO_URL, required=False, label=CREATE_LOGO_URL)
  docUrl = forms.CharField(max_length=LENGTH_DOC_URL, required=False, label=CREATE_DOC_URL)

# Form used for editing a paper
class EditPaperForm(forms.Form):
  id = forms.IntegerField(required=True, label="Paper ID")
  title = forms.CharField(max_length=LENGTH_TITLE, required=False, label=EDIT_TITLE)
  authors = forms.CharField(max_length=LENGTH_AUTHORS, required=False, label=EDIT_AUTHORS)
  abstract = forms.CharField(max_length=LENGTH_ABSTRACT, required=False, label=EDIT_ABSTRACT)
  logoUrl = forms.CharField(max_length=LENGTH_LOGO_URL, required=False, label=EDIT_LOGO_URL)
  docUrl = forms.CharField(max_length=LENGTH_DOC_URL, required=False, label=EDIT_DOC_URL)

  # setting id as readonly - "disabled" does not work, since it is not returned from the template
  def __init__(self, *args, **kwargs):
    super(EditPaperForm, self).__init__(*args, **kwargs)
    self.fields['id'].widget.attrs['readonly'] = True

# Form used for deleting a paper
class DeletePaperForm(forms.Form):
  id = forms.IntegerField(required=True, label="Paper ID")