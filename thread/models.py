from django.db import models

from django.contrib.auth import get_user_model
# Create your models here
#get current user
User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(max_length=1000, blank=True)
    profile_pics = models.ImageField(upload_to='profile_images', default='anon.png')
    location_city = models.CharField(max_length=100, blank=user)

    def __str__(self):
        return (f"{self.user.username}  ------   {self.user.email}")