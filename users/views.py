from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as dj_login, authenticate, logout
from users.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.contrib import messages
from django.template import loader
from users.models import Account
from django.urls import reverse
from todos.models import Todo
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        all_users = Account.objects.all()
    else:
        all_users = None
    template = loader.get_template('users/home.html')
    return HttpResponse(template.render({"users":all_users}, request))

def registration_view(request):
    context = {}
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=raw_password)
                dj_login(request, account)
                return HttpResponseRedirect(reverse('users:index'))
            else:
                context['registration_form'] = form
        else:
            form = RegistrationForm()
            context['registration_form'] = form
        return render(request=request, template_name="users/register.html", context={"registration_form":form})
    else:
        return redirect('users:index')

def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('users:index')
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            email.lower()
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                dj_login(request, user)
                return redirect('users:index')
    
    else:
        form = AccountAuthenticationForm()
    return render(request, 'users/login.html', context={'form':form})

def logout_view(request):
    logout(request)
    return redirect('users:index')

def account_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context['success_message'] = "Account Updated"
        
    else:
        form = AccountUpdateForm(initial={"email": request.user.email, "username":request.user.username})
    
    todo = Todo.objects.filter(author=request.user)
    context["account_form"] = form
    context["todos"] = todo
    return render(request, "users/account.html", context)

def must_authenticate_view(request):
    return render(request, "users/must_authenticate.html", context={})
