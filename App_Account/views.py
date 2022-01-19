from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from App_Account.forms import *
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from App_Account.models import Profile
def SignupView(request):
    if request.method=="POST":
        username_=request.POST['username']
        email_=request.POST['email']
        password_=request.POST['password']
        password2_=request.POST['password2']
        if User.objects.filter(username=username_).exists():
            messages.success(request, "Email & username is registered")
            return redirect('App_Account:signup')
        elif password_!=password2_:
            messages.success(request, "password not matching")
            return redirect('App_Account:signup')

        else:
            user=User.objects.create_user(
                username=username_,email=email_,password=password_
            )
            user.save()
            pro=Profile.objects.create(user=user)
            pro.save()
            login(request,user)
            messages.success(request,"Account Create succesfully")
            return redirect('App_Account:signup')
    else:
        return render(request,'App_Account/signup.html')
def LoginpView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('App_Quiz:home')
        else:
            messages.info(request, "Enter correct username and password")
            return redirect('App_Account:login')

    else:
        return render(request, 'App_Account/login.html')
def Logout_view(request):
    logout(request)
    return redirect('App_Account:login')
def DashBoard(request):
    return render(request,'App_Account/dashboard.html')

def UpdateProfile(request):
    if request.method=="POST":
        pro=Profile.objects.get(user=request.user)
        email=request.POST.get('email')
        firstname=request.POST.get('first')
        lastname=request.POST.get('last')
        photo=request.user.profile.photo
        if len(request.FILES)!=0:
            photo=request.FILES['photo']
        print(photo)
        request.user.first_name=firstname
        request.user.last_name=lastname
        request.user.email=email
        request.user.save()
        pro.photo=photo
        pro.save()
        messages.success(request,"Profile updated",extra_tags="profile")
        return redirect(request.POST['next'])
    return render(request,'App_Account/update.html')

def About(request):
    return render(request,'App_Account/about.html')