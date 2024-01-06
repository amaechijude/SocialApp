from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile

# Create your views here.


def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email =  request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        #confirm password match and unique username & email
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is taken')
                return redirect('sign_up')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is taken')
                return redirect('sign_up')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                #create a profile for the user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user.id)
                new_profile.save()
                messages.info(request, 'Your profile is created successfully')
                return redirect('sign_up')

        else:
            messages.info(request, 'Passwords mismatch')
            return redirect('sign_up')


    return render(request, 'signup.html')

def login_user(request):
    return render(request, 'login.html')