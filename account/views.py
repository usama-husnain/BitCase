from django.contrib.auth import authenticate, login as auth_login
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
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


@login_required(login_url='/login')
def profile(request):
   
    return render(request, 'account/profile.html')


@login_required(login_url='/login')
def profile_update(request):
    
    context={'profile':None}
    user_profile = Profile.objects.filter(user_id=request.user.id)
    # print(user_profile[0])
    if user_profile.exists():
        user_profile = user_profile[0]
        context['profile']=user_profile
        if request.method=='POST':
            form = ProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()

                return redirect('profile')
        
    else:
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Set the user for the profile
            profile.save()
            return redirect('profile')  # Redirect to a success page
        
    return render(request, 'account/create_update_profile.html', context)