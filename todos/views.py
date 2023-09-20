from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from todos.forms import *
from django.contrib.auth.decorators import login_required
from users.models import Account as User

# Create your views here.

def create_todo(request):

    context = {}
    if not request.user.is_authenticated:
        return redirect('user:must_authenticate')
    
    form = create_task_form(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        userz = User.models.filter(email=request.user.email).first()
        task.user = userz
        task.save()
        form = create_task_form()
        context['success_message'] = 'Task Created!'
    context['form'] = form

    return render(request, 'todo/create.html', context)

@login_required
def edit_todo(request, task_id):
    context = {}
    todo = get_object_or_404(Todo, pk=task_id)
    if not request.user.email == todo.user.email:
        return HTTPResponse('You are not the owner of this Task.')
    if request.POST:
        form = task_update_form(request.POST or None, instance=todo)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            todo = obj
    form = task_update_form(
        initial={
            'title':todo.title,
            'description': todo.description,
            'priority': todo.priority,
        }
    )
    return render(request, 'todo/update.html', context={'success_message':'Task Updated!', 'form':form})

@login_required
def delete_todo(request, task_id):
    context = {}
    user = request.user.email
    todo = get_object_or_404(Todo, pk=task_id)
    if not request.user.email == todo.user.email:
        return HttpResponse('You are not the onwer of this todo')
    if request.POST:
        todo.delete()
        return redirect('users:index')
    return HttpResponse('Invalid request method')

