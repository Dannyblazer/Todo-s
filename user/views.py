from django.shortcuts import render, redirect
from django.contrib.auth import login as dj_login, authenticate, logout
from django.urls import reverse
from .models import User
from .forms import *
from django.http import HttpResponseRedirect
# Create your views here.

def registration_view(request):
    context = {}
    if not request.user.is_authenticatd:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=raw_password)
                #Automatic login after authentication
                dj_login(request, account)
                return HttpResponseRedirect(reverse('general:home'))
            else:
                context['registration_form'] = form
        else:
            form = RegistrationForm()
            context['registration_form'] = form
        return render(request=request, template_name='user/registrations.html', context={"registration_form":form})
    else:
        return redirect('general:home')

def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('general:home')
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email'].lower()
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                dj_login(request, user)
                return redirect('general:home')
    else:
        form = UserAuthenticationForm()
    return render(request, 'user/login.html', context={'form':form})

def logout(request):
    logout(request)
    return redirect('general:home')

def account_view(request):
    if not request.user.is_authenticated:
        return redirect('general:home')
    context = {}
    if request.POST:
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context['success_message'] = 'Account Updated'

    else:
        form = UserUpdateForm(initial={'email':request.user, 'username':request.user.username})

    context['account_form'] = form
    return render(request, 'user/account.html', context)

def must_authenticate_view(request):
    return render(request, 'user/must_authenticate.html', context={})

