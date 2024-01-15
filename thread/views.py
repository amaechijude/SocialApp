from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile

# Create your views here.

#@login_required(login_url='login_user')
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.info(request, 'You are logged in')
            return redirect('home')
        else:
            messages.info(request, 'Profile not found')
            return redirect('login_user')
    else:
        return render(request, 'login.html')

#log out
@login_required(login_url='login_user')    
def logout_user(request):
    logout(request)
    return redirect('login_user')


@login_required(login_url='login_user')
def settings_user(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('profile_pics') == None:
            profile_pics = user_profile.profile_pics
            bio = request.POST['bio']
            location_city = request.POST['location_city']

            user_profile.profile_pics = profile_pics
            user_profile.bio = bio
            user_profile.location_city = location_city
            user_profile.save()

        elif request.FILES.get('profile_pics') != None:
            image = user_profile.profile_pics
            bio = request.POST['bio']
            location_city = request.POST['location_city']

            user_profile.profile_pics = image
            user_profile.bio = bio
            user_profile.location_city = location_city
            user_profile.save()
        return redirect('settings_user')
        
    return render(request, 'settings.html', {'user_profile': user_profile})