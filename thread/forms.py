from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')


class UpdateProfile(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    bio = forms.CharField()
    profile_pics = forms.ImageField()
    location_city = forms.CharField()
    class Meta:
        model = Profile
        exclude = ('user', 'id_user')