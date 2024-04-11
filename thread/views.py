from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, PostModel, LikePost, CommentModel, FollowerModel, Story
from .forms import UserForm, UpdateProfile, PostForm
from datetime import datetime, timezone

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .serializers import StorySerializer
import json
# Create your views here

User = get_user_model()

def stories(request):
    stories = Story.objects.all()
    storiesSerializer = StorySerializer(stories, many=True).data
    context = {"data": json.dumps(storiesSerializer), "stories":stories,}
    return render(request,'stories.html',context)
    #return JsonResponse(storiesSerializer, safe=False)

def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        following = FollowerModel.objects.filter(follower=username)
        all_post = PostModel.objects.all()
        likes = LikePost.objects.filter(username=username)
        stories = Story.objects.all()
        all_profile = Profile.objects.all()
        context = {
            "all_post": all_post,
            #"user": user,
            "likes": likes,
            "following": following,
            "all_profile": all_profile,
            "stories": stories,
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
        
  
        messages.info(request, "{Error: Could not sign up}")
        return redirect('sign_up')    

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
    posts = PostModel.objects.filter(author=profile)
    post_len = len(posts)
    pk = str(user.username)
    fans = FollowerModel.objects.filter(user=pk)
    followings = FollowerModel.objects.filter(follower=pk)
    fans_count = len(fans)
    followings_count = len(followings)
    context = {
        "profile": profile,
        "posts":posts,
        "post_len": post_len,
        "fans_count": fans_count,
        "fans": fans,
        "followings": followings,
        "followings_count": followings_count,
        }
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
    return render(request, 'settings.html', {"form":form, "profile":profile})

@login_required(login_url='login_user')
def create_post(request):
    if request.method == 'POST':
        author = request.user.profile
        content = request.POST['content']
        image = request.FILES.get('image')

        if content != None:
            if image != None or image == None:
                new_post = PostModel.objects.create(author=author,
                                                content=content,
                                                image=image)
                new_post.save()
            
                messages.success(request, "Post created")
                return redirect('home')
        messages.info(request, "Text box should not be empty")
        return redirect('create_post')
    return render(request, 'post.html')
    

@login_required(login_url='login_user')
def post_view(request, pk):
    post_object = PostModel.objects.get(postID=pk)
    comments = CommentModel.objects.filter(post=post_object)
    utc_time = post_object.created_at 
    iso_format = utc_time.isoformat()
    context = {
            "post_object":post_object,
            "comments":comments,
            "iso_format": iso_format, 
            }
    return render(request, 'post_detail.html', context)

@login_required(login_url='login_user')
def comment(request):
    if request.method == 'POST':
        author = request.user.profile
        postID = request.POST['postID']
        post = PostModel.objects.get(postID=postID)
        content = request.POST['content']

        new_comment = CommentModel.objects.create(author=author, post=post,content=content)
        new_comment.save()
        post.num_of_comments += 1
        messages.success(request,"Comment added")
        url = 'post_view/'
        return redirect(f"{url}{postID}")


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
    return redirect(f'home')


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
    followings = FollowerModel.objects.filter(follower=pk)
    fans_count = len(fans)
    followings_count = len(followings)
    context = {
        "user_object": user_object,
        "user_profile": user_profile,
        "user_post": user_post,
        "user_post_len": user_post_len,
        "image_url": image_url,
        "follow_check": follow_check,
        "fans_count": fans_count,
        "fans": fans,
        "followings": followings,
        "followings_count": followings_count,

        }
    return render(request, 'profile.html', context)


@login_required(login_url='login_user')
def follow(request):
    if request.method == 'POST':
        follower = request.user.username
        user = request.POST['user']
        user = user

        if follower == user:
            return redirect('account_setting')
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

        return redirect('home')
    else:
        return render(request, 'story.html')
