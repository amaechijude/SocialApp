from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post
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
    title = forms.CharField(required=True)
    content = forms.CharField(required=False)
    image = forms.FileField(required=False)
    class Meta:
        model = Post
        exclude = ('postID', 'created_at',)