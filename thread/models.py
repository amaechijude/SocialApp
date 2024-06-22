from django.db import models
from datetime import datetime
from django.core.validators import URLValidator

from django_resized import ResizedImageField # Compreess image

# Create your models here

#get current user
from django.contrib.auth import get_user_model
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    profile_pics = ResizedImageField(quality=70,upload_to='profile_images') 
    github_url = models.URLField(validators=[URLValidator()], max_length=300, blank=True)
    linkedin_url = models.URLField(validators=[URLValidator()], max_length=300, blank=True)

    USERNAME_FIELD = 'user.username'

    def __str__(self):
        return (f"{self.user.username}")


class PostModel(models.Model):
    postID = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    image = ResizedImageField(blank=True,quality=70,upload_to='profile_posts')
    created_at = models.DateTimeField(auto_now=True)
    num_of_likes = models.IntegerField(default=0)
    num_of_comments = models.IntegerField(default=0)
    #slug = models.SlugField(unique=True,)
    # tags = TaggableManager()

    def __str__(self):
        return (f"{self.content}")


class CommentModel(models.Model):
    post = models.ForeignKey('PostModel', on_delete=models.CASCADE)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.author.user.username}")


class LikePost(models.Model):
    postID = models.IntegerField()
    username = models.CharField(max_length=100)

    def __str__(self):
        return (f"{self.username}")


class FollowerModel(models.Model):
    follower = models.CharField(max_length=150)
    user = models.CharField(max_length=150)

    def __str__(self):
        return f"User: {self.user}, ---- follower : {self.follower}"

class Story(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.CharField(blank=True, max_length=250)
    image = ResizedImageField(blank=False, quality=70, upload_to='stories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural ="Stories"
    
    def __str__(self):
        return f"{self.author.user.username} ---  {self.caption}"
