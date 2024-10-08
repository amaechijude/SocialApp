from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, PostModel, LikePost, CommentModel, FollowerModel, Story
from .forms import UpdateProfile, PostForm, StoryForm, UserForm
from django.contrib.auth.models import User
from rest_framework import status as st


from django.core.paginator import Paginator
# Create your views here

def home(request):
    username = request.user.username
    post = PostModel.objects.all().order_by('-created_at')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(post, 20)
    all_post = paginator.get_page(page_number)
    likes = LikePost.objects.filter(username=username)

    #story
    stories = Story.objects.all().order_by('-created_at')
    all_profile = Profile.objects.all()

    form = StoryForm()
    context = {
        "all_post": all_post, "likes": likes, "stories": stories,
        "form": form, "all_profile": all_profile,
        }
    return render(request, 'home.html', context)


# Sign up a new user
def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save() # new user saved

            #create profile
            username = form.cleaned_data['username']
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save() # created profile for the above user

            # Redirect to login page
            messages.info(request, 'Profile created. you can now login')
            return redirect('login_user')
        
    form = UserForm()
    return render(request, 'signup.html', {"form": form})


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
    
    return render(request, 'login.html')

#log out
@login_required(login_url='login_user')    
def logout_user(request):
    logout(request)
    return redirect('login_user')

#delete account
@login_required(login_url='login_user')
def del_account(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_staff:
            messages.info(request,"Can't delete admin account")
            return redirect('home')
        
        user.is_active = False
        messages.info(request, "Account Set inactive")
        return redirect('sign_up')
    return redirect('login_user')


# Logged in user deatails
# @login_required(login_url='login_user')
# def details(request):
    user = request.user; profile = user.profile
    posts = PostModel.objects.filter(author=profile)
    post_len = len(posts); pk = str(user.username)
    fans = FollowerModel.objects.filter(user=pk)
    followings = FollowerModel.objects.filter(follower=pk)
    fans_count = len(fans); followings_count = len(followings)
    context = {
        "profile": profile, "posts":posts, "post_len": post_len,
        "fans_count": fans_count, "fans": fans, "followings": followings,
        "followings_count": followings_count,
        }
    return render(request, 'details.html', context)

# Account/ profile settings
@login_required(login_url='login_user')
def account_setting(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        form = UpdateProfile(request.POST, request.FILES or None, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")
            return redirect('profile', pk=request.user.username)
        
        messages.error(request, f"{form.errors}")
        return redirect('home')
    form = UpdateProfile(instance=profile)
    return render(request, 'settings.html', {"form":form, "profile":profile})


# Create a post
@login_required(login_url='login_user')
def create_post(request):
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



# Vieew a single post
def post_view(request, pk):
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

# comment on a post
@login_required(login_url='login_user')
def comment(request, pk):
    if request.htmx:
        author = request.user.profile
        postID = pk
        post = PostModel.objects.get(postID=postID)
        content = request.POST['content']

        new_comment = CommentModel.objects.create(author=author, post=post,content=content)
        new_comment.save()
        post.num_of_comments += 1

        comments = CommentModel.objects.filter(post=post)
        context = {
                "comments":comments,
                }
        return render(request, 'partial/comment.html', context)
 

# delete a post
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
    

# # Like a post   
def like_post(request, postID):
    if request.user.is_authenticated:
        username = request.user.username
        post = get_object_or_404(PostModel, postID=postID)

        like_check = LikePost.objects.filter(username=username, postID=postID).first()

        if like_check == None:
            new_like = LikePost.objects.create(username=username, postID=postID)
            new_like.save()
            post.num_of_likes += 1; post.save()
            data = {"num_of_likes": post.num_of_likes,"message": "Liked", "postID": postID}
            return JsonResponse(data)
        
        like_check.delete()
        post.num_of_likes -= 1; post.save()
        data = {"num_of_likes": post.num_of_likes,"message": "Unlike", "postID": postID}
        return JsonResponse(data)
    return JsonResponse({"err": "You need to log in"})



# User Profile
@login_required(login_url='login_user')
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



#Follow / unfollow
@login_required(login_url='login_user')
def follow(request):
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


@login_required(login_url='login_user')
def story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES or None)
        if form.is_valid():
            new_story = form.save(commit=False)
            author = request.user.profile
            new_story.author = author
            new_story.save()
            messages.success(request, "Story Created")
            return redirect('home')
        messages.error(request, f"{form.errors}")
        return redirect('home')
    messages.info(request, "Method not allowed")
    return redirect('home')



# def story(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             form = StoryForm(request.POST, request.FILES or None)
#             if form.is_valid():
#                 new_story = form.save(commit=False)
#                 author = request.user.profile
#                 new_story.author = author
#                 new_story.save()

#                 context = {
#                     'authorImage': f"{new_story.author.profile_pics.url}",
#                     'authorUsername': f"{new_story.author.user.username}",
#                     'storyCaption': f"{new_story.caption}",
#                     'storyImage': f"{new_story.image.url}"
#                 }
#                 return JsonResponse(context, status=st.HTTP_201_CREATED)
#             return JsonResponse(form.errors, status=st.HTTP_400_BAD_REQUEST)
#         return JsonResponse({"method": "Method not allowed"}, status=st.HTTP_405_METHOD_NOT_ALLOWED)
#     return JsonResponse({"err": "You need to login"}, status=st.HTTP_401_UNAUTHORIZED)

