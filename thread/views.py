from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, PostModel, LikePost, FollowerModel, Story
from .forms import UserForm, UpdateProfile, PostForm

# Create your views here

User = get_user_model()

def foot(request):
    return render(request, 'footnote.html')

def index(request):
    #user = request.user
    #following = FollowerModel.objects.filter(follower=user)
    all_post = PostModel.objects.all()
    likes = reversed(LikePost.objects.all())
    unique_likes = list(likes)
    all_profile = Profile.objects.all()
    stories = Story.objects.all()
    context = {
            "all_post": all_post,
            #"user": user,
            #"unique_likes": unique_likes,
            #"following": following,
            #"all_profile": all_profile,
            "stories": stories,
            }
    return render(request, 'index.html', context)
def home(request):
    if request.user.is_authenticated:
        #user = request.user
        #following = FollowerModel.objects.filter(follower=user)
        all_post = PostModel.objects.all()
        #unique_likes = LikePost.objects.all()
        #all_profile = Profile.objects.all()
        context = {
            "all_post": all_post,
            #"user": user,
            #"unique_likes": unique_likes,
            #"following": following,
            #"all_profile": all_profile,
            }
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
    profile = user.profile
    image_url = profile.profile_pics.url
    context ={"profile": profile, "image_url": image_url}
    return render(request, 'details.html', context)

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

"""
@login_required(login_url='login_user')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            author = request.user.profile
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']

            new_post = PostModel.objects.create(author=author, content=content, image=image)
            new_post.save()
            
            messages.success(request, "Post created")
            return redirect('home')
        messages.info(request, "Post was not created")
    form = PostForm()
    context = {"form": form}
    return render(request, 'post.html', context)
"""

@login_required(login_url='login_user')
def create_post(request):
    if request.method == 'POST':
        author = request.user.profile
        content = request.POST['content']
        image = request.FILES.get('image')

        if image != None:
            new_post = PostModel.objects.create(author=author, content=content, image=image)
            new_post.save()
            
            messages.success(request, "Post created")
            return redirect('index')
        messages.info(request, "Post was not created")
        return redirect('index')
    return render(request, 'post.html')
    

@login_required(login_url='login_user')
def post_view(request, pk):
    post_object = PostModel.objects.get(postID=pk)
    return render(request, 'post_detail.html', {"post_object": post_object})

@login_required(login_url='login_user')
def delete_post(request, pk):
    user = request.user.profile
    post_object = PostModel.objects.get(postID=pk)
    if user == post_object.author:
        post_object.delete()
        messages.info(request, "Post deleted successfully")
        return redirect('home')
    else:
        messages.info(request, "Can't delete, You aren't the Author")
        return redirect('home')

@login_required(login_url='login_user')    
def like_post(request, pk):
    username = request.user.username
    post = PostModel.objects.get(postID=pk)

    like_check = LikePost.objects.filter(username=username, postID=pk).first()
    if like_check == None:
        new_like = LikePost.objects.create(username=username, postID=pk)
        new_like.save()
        post.num_of_likes += 1
        post.save()
    else:
        like_check.delete()
        post.num_of_likes -= 1
        post.save()
    return redirect('index')


def profile(request,pk):
    pk = str(pk)
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_post = PostModel.objects.filter(author=user_profile)
    user_post_len = len(user_post)
    image_url = user_profile.profile_pics.url

    follower = request.user.username
    user = pk

    if FollowerModel.objects.filter(follower=follower, user=user):
        follow_check = "Unfollow"
    else:
        follow_check = "Follow"
        
    fans = FollowerModel.objects.filter(user=pk)
    fans_count = len(fans)
    context = {
        "user_object": user_object,
        "user_profile": user_profile,
        "user_post": user_post,
        "user_post_len": user_post_len,
        "image_url": image_url,
        "follow_check": follow_check,
        "fans_count": fans_count,
        "fans": fans,

        }
    return render(request, 'profile.html', context)


@login_required(login_url='login_user')
def follow(request):
    if request.method == 'POST':
        follower = request.user.username
        user = str(request.POST['user'])

        if follower == user:
            return redirect('details')
        else:
            if FollowerModel.objects.filter(follower=follower, user=user).first():
                delete_follower = FollowerModel.objects.get(follower=follower, user=user)
                delete_follower.delete()
                return redirect('profile/'+user)
            else:
                new_follower = FollowerModel.objects.create(follower=follower, user=user)
                new_follower.save()
                return redirect('profile/'+user)
    else:
        return redirect('home')


@login_required(login_url='login_user')
def story(request):
    if request.method == 'POST':
        author = request.user.profile
        caption = request.POST['caption']
        image = request.FILES.get('image')

        new_story = Story.objects.create(author=author,caption=caption,image=image,)
        new_story.save()
        messages.success(request, "Story created")

        return redirect('index')
    else:
        return render(request, 'story.html')
