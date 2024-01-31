from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password1 = models.CharField(max_length=25)
    password2 = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    bio = models.TextField(max_length=1000, blank=True)
    profile_pics = models.ImageField(upload_to='profile_images', default='anon.png')
    location_city = models.CharField(max_length=100, blank=user)

    def __str__(self):
        return (f"{self.user.username}  ------   {self.user.email}")