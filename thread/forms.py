from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'id_user')