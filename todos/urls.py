from django.urls import path
from todos.views import *
app_name = 'todos'

urlpatterns = [
    path('create/', create_todo, name='create'),
    path('update/', edit_todo, name='edit'),
  ]
