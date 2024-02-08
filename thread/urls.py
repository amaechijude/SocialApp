from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('details', views.details, name='details'),
    path('account_setting', views.account_setting, name='account_setting'),
    path('create_post', views.create_post, name='create_post'),
    path('like_post', views.like_post, name='like_post')
]
