from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class ProfileForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)

    class Meta:
        model = Profile
        fields = ('email', 'username', 'password1', 'password2')