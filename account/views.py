from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .validation import *
# Create your views here.


def login(request):
    if request.method == 'POST':
        form = LoginFormValidation(request.POST)
        # print(form.errors)
    
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # user = User.objects.filter(email=email).first
            user = authenticate(username=email, password=password)
       
            if user:
                auth_login(request, user)
                request.session['login']="Successfully Login! Welcome to Bit-Case."
                if(request.session['next']):
                    return redirect(request.session['next'])
                return redirect('/welcome')
            else:
                messages.success(request, "Credentials you entered are invalid!")
                return redirect("login")
        else:
            
            return render(request, 'account/login.html', {'form':form})
    
    if(request.GET.get('next')):
        param = request.GET.get('next')
        request.session['next'] = param
    else:
        request.session['next'] = None

    if request.user.is_authenticated:
        return redirect('welcome')
    
    return render(request, 'account/login.html')

def register(request):
    if(request.method=='POST'):
        
        form = RegisterFormValidation(request.POST)
        # print(form.errors)
       
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(email=email, username=email)
            user.set_password(password)
            user.save()
            return redirect("login")
        else:
            
            return render(request, 'account/register.html', {'form':form})
    
    return render(request, 'account/register.html')


def logout_view(request):
    logout(request)
    return redirect("login")