from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, PostModel
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UpdateProfile(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "firstName"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "lastName"}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "id": "bio", "rows": "3"}))
    profile_pics = forms.FileField(required=False, widget=forms.FileInput(attrs={"class": "form-control", "id": "profileImage"}))

    class Meta:
        model = Profile
        exclude = ('user', 'id_user')
        #fields = ('first_name','last_name','bio','profile_pics','location_city')


class PostForm(forms.ModelForm):
    content = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={"id":"teet-text", "placeholder":"What's Happening"}), label="")
    image = forms.FileField(required=True, widget=forms.widgets.Textarea(attrs={"id":"image-input"}), label="image-input")
    class Meta:
        model = PostModel
        exclude = ('postID','created_at', 'author', 'num_of_likes')
