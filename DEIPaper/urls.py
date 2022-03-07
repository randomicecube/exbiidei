from django.urls import path
from . import views

urlpatterns = [
  # home page redirections
  path('home/', views.index, name='home'),
  path('', views.index, name='index'),
  # general redirections
  path('list-all-papers/<int:first_id>-<int:last_id>-<int:prev>/', views.list_all_papers, name='list-papers-parameters'),
  path('list-all-papers/', views.list_all_papers, name='list-all-papers'),
  path('list-specific-paper/', views.list_specific_paper, name='list-specific-paper'),
  path('create-paper/', views.create_paper, name='create-paper'),
  path('edit-paper/', views.edit_paper, name='edit-paper'),
  path('delete-paper/', views.delete_paper, name='delete-paper'),
]