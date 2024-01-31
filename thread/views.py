from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import UserForm

# Create your views here.
User = get_user_model()
#@login_required(login_url='login_user')
def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid:
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            return redirect('home')
        
        form = UserForm()
        content = {"form":form}
        messages.info(request, "{Error: Could not sign up}")
        return render(request, 'signup.html', content)    

    form = UserForm()
    content = {"form":form}
    return render(request, 'signup.html', content)

#login view
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        user = authenticate(username=username, password=password)
        
        if user != None:
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

"""
@login_required(login_url='login_user')
def settings_user(request, user=''):
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
        
    return render(request, 'settings.html', {'user_profile': user_profile})"""