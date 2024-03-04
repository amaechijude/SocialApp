from django.db import models
from datetime import datetime

from django_resized import ResizedImageField # Compreess image

from django.contrib.auth import get_user_model
# Create your models here

#get current user
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    profile_pics = ResizedImageField(size=[300, 300], quality=70, upload_to='profile_images', default='anon.png') 
   #profile_pics = models.ImageFieldi(upload_to='profile_images', default='anon.png')
    location_city = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = 'user.username'

    def __str__(self):
        return (f"{self.user.username}")
    

class PostModel(models.Model):
    postID = models.AutoField(primary_key=True)
    author = models.CharField(max_length=150, default='current_user')
    title = models.CharField(blank=True, max_length=150)
    content = models.TextField(blank=True, default="Post something")
    image = ResizedImageField(blank=True, size=[400, 400], quality=70, upload_to='profile_posts')
    created_at = models.DateTimeField(default=datetime.now)
    num_of_likes = models.IntegerField(default=0)
    #full_name = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return (f"{self.title}")

class LikePost(models.Model):
    postID = models.IntegerField()
    username = models.CharField(max_length=100)

    def __str__(self):
        return (f"{self.username}")


class FollowerModel(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return f"User: {self.user}, ---- follower : {self.follower}"
