from django import forms
from PIL import Image, ImageFile, ImageOps, ExifTags
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, PostModel, Story
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    username = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'username', 'id':'username'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address', 'id':'email'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'id':'password1'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password', 'id':'password2'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

 


class UpdateProfile(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "firstName"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "lastName"}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "id": "bio", "rows": "3"}))
    profile_pics = forms.FileField(required=False, widget=forms.FileInput(attrs={"class": "form-control", "id": "profileImage"}))

    class Meta:
        model = Profile
        exclude = ('user', 'id_user')
        #fields = ('first_name','last_name','bio','profile_pics','github_url')


class PostForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={"maxlength":"300", "id": "tweet-text", "placeholder":"What's happening?"}))
    image = forms.FileField(required=False, widget=forms.FileInput(attrs={"accept":"image/*", "id": "image-input"}))
    class Meta:
        model = PostModel
        exclude = ('postID','created_at', 'author', 'num_of_likes', 'num_of_comments')

class StoryForm(forms.ModelForm):
    caption = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"id":"create-post", "placeholder":"Add Story", "class":"image_file"}), label="")
    image = forms.FileField(required=True, widget=forms.widgets.FileInput(attrs={"id":"image"}), label="for-image")
    
    class Meta:
        model = Story
        exclude = ('author', 'created_at')
