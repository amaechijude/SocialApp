from django.db import models

from django.contrib.auth import get_user_model
# Create your models here

#get current user
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    profile_pics = models.ImageField(upload_to='profile_images', default='anon.png')
    location_city = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'user.username'

    def __str__(self):
        return (f"{self.user.username}")
    

    class PostModel(models.Model):
        postID = models.AutoField(primary_key=True)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        title = models.CharField(max_length=100)
        content = models.TextField(blank=True, default="Post something")
        image = models.ImageField(upload_to='profile_posts', blank=True)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return (f"{self.title}")