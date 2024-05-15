from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, PostModel, LikePost, CommentModel, FollowerModel, Story
from .forms import UpdateProfile, PostForm, StoryForm
from datetime import datetime, timezone
from django.contrib.auth.models import User, auth
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .serializers import StorySerializer
import json

# Create your views here


def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        #following = FollowerModel.objects.filter(follower=username)
        all_post = PostModel.objects.all()
        likes = LikePost.objects.filter(username=username)
        stories = Story.objects.all()
        all_profile = Profile.objects.all()
        form = StoryForm()
        context = {
            "all_post": all_post,
            "likes": likes,
            "stories": stories,
            "form": form,
            "all_profile": all_profile,
            }
        return render(request, 'home.html', context)
    else:
        all_post = PostModel.objects.all()
        #likes = LikePost.objects.filter(username=username)
        stories = Story.objects.all()
        all_profile = Profile.objects.all()
        form = StoryForm()
        context = {
            "all_post": all_post,
            #"likes": likes,
            "stories": stories,
            "form": form,
            "all_profile": all_profile,
            }
        messages.info(request, "Signup / Login for full experience")
        return render(request, 'home.html', context)

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return redirect('sign_up')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Error: email taken")
                return redirect('sign_up')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()

                #create profile
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                #Authenticate and login
                new_user = authenticate(username=username, password=password)
                login(request, new_user)
                return redirect('details')
            
        else:   
            messages.info(request, "Password mismatch")
            return redirect('sign_up')
    else:
        return render(request, 'signup.html')

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
    if request.user.is_authenticated:
        logout(request)
        return redirect('login_user')
    return redirect('login_user')

#delete account
@login_required(login_url='login_user')
def del_account(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_staff:
            messages.info(request,"Can't delete admin account")
            return redirect('home')
        else:
            user.delete()
            messages.info(request, "Account Deleted")
            return redirect('sign_up')
    return redirect('login_user')

@login_required(login_url='login_user')
def details(request):
    if request.user.is_authenticated:
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
    return redirect('login_user')

@login_required(login_url='login_user')
def account_setting(request):
    if request.user.is_authenticated:
        user = request.user
        profile = user.profile
        if request.method == 'POST':
            form = UpdateProfile(request.POST or None, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
            return redirect('details')
        form = UpdateProfile(instance=profile)
        return render(request, 'settings.html', {"form":form, "profile":profile})
    return redirect('login_user')

@login_required(login_url='login_user')
def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            author = request.user.profile
            content = request.POST['content']
            image = request.FILES.get('image')

            if image != None:
                new_post = PostModel.objects.create(author=author,content=content,image=image)
                new_post.save()
            
                messages.success(request, "Post created")
                return redirect('home')
            messages.info(request, "Attach image")
            return redirect('create_post')
        form = PostForm()
        context = {"form":form}
        return render(request, 'post.html', context)
    return redirect('login_user')
    

#@login_required(login_url='login_user')
def post_view(request, pk):
    #if request.user.is_authenticated:
    post_object = PostModel.objects.get(postID=pk)
    comments = CommentModel.objects.filter(post=post_object)
    comment_num = len(comments)
    utc_time = post_object.created_at 
    iso_format = utc_time.isoformat()
    context = {
        "post_object":post_object,
        "comments":comments,
        "comment_num":comment_num, 
        "iso_format": iso_format, 
            }
    return render(request, 'post_detail.html', context)
    #return redirect('login_user')

@login_required(login_url='login_user')
def comment(request):
    if request.user.is_authenticated:
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
    messages.info(request, "Signup / Login for full experience")
    return redirect('login_user')


@login_required(login_url='login_user')
def delete_post(request, pk):
    if request.user.is_authenticated:
        user = request.user.profile
        post_object = PostModel.objects.get(postID=pk)
        if user == post_object.author:
            post_object.delete()
            messages.info(request, "Post deleted successfully")
            return redirect('home')
        else:
            messages.info(request, "Can't delete, You aren't the Author")
            return redirect('home')
    return redirect('login_user')

@login_required(login_url='login_user')    
def like_post(request, pk):
    if request.user.is_authenticated:
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
    messages.info(request, "Signup / Login for full experience")
    return redirect('login_user')


def profile(request,pk):
    if request.user.is_authenticated:
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
    else:
        pk = str(pk)
        user_object = User.objects.get(username=pk)
        user_profile = Profile.objects.get(user=user_object)
        user_post = PostModel.objects.filter(author=user_profile)
        user_post_len = len(user_post)
        image_url = user_profile.profile_pics.url

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
            #"follow_check": follow_check,
            "fans_count": fans_count,
            "fans": fans,
            "followings": followings,
            "followings_count": followings_count,
            }
        messages.info(request, "Signup / Login for full experience")
        return render(request, 'profile.html', context)


    #return redirect('login_user')

@login_required(login_url='login_user')
def follow(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            follower = str(request.user.username)
            user = request.POST['user']
            user = str(user)

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
    messages.info(request, "Signup / Login for full experience")
    return redirect('login_user')


@login_required(login_url='login_user')
def story(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = StoryForm(request.POST, request.FILES)
            if form.is_valid():
                author = request.user.profile
                caption = form.cleaned_data['caption']
                image = form.cleaned_data['image']

                new_story = Story.objects.create(author=author,caption=caption,image=image,)
                new_story.save()
                messages.success(request, "Story created")

                return redirect('home')
            messages.info(request, "Error, Add Image")
            return redirect('home')
        else:
            return render(request, 'home.html')
    messages.info(request, "Signup / Login for full experience")
    return redirect('login_user')


def tag_list(request, pk):
    tag = Tag.objects.get(slug=pk)
    objects = tag.tagged_objects.all()

    context = {
            'tag': tag,
            'object_list': objects,
            }

    return None #render(request, "tagged_object_list.html", context)
