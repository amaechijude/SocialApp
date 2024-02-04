from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Post
from .forms import UserForm, UpdateProfile, PostForm

# Create your views here
User = get_user_model()
#@login_required(login_url='login_user')
def home(request):
    if request.user.is_authenticated:
        all_post = Post.objects.all()
        context = {"all_post": all_post}
        return render(request, 'home.html', context)
    else:
        return redirect('login_user')

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

@login_required(login_url='login_user')
def details(request):
    user = request.user
    print(user)
    profile = user.profile
    profile_data = {
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "bio": profile.bio,
        "profile_pics": profile.profile_pics,
        "location_city":profile.location_city
    }
    image_url = profile.profile_pics.url
    context ={"profile_data": profile_data, "image_url": image_url}
    return render(request, 'profile.html', context)


@login_required(login_url='login_user')
def account_setting(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        form = UpdateProfile(request.POST or None, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        return redirect('details')
    form = UpdateProfile(instance=profile)
    return render(request, 'settings.html', {"form":form})


@login_required(login_url='login_user')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Post created")
            return redirect('home')
    form = PostForm()
    context = {"form": form}
    return render(request, 'post.html', context)