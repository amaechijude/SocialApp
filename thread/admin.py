from django.contrib import admin
from .models import Profile, PostModel, LikePost, FollowerModel, Story

# Register your models here.
admin.site.register(Profile)
admin.site.register(PostModel)
admin.site.register(LikePost)
admin.site.register(FollowerModel)
admin.site.register(Story)