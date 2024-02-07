from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, PostModel
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'profile_pics', 'location_city')


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        exclude = ('postID', 'created_at', 'author', 'num_of_likes')