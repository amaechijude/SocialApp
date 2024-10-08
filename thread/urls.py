from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    # path('details', views.details, name='details'),
    path('account_setting', views.account_setting, name='account_setting'),
    path('create_post', views.create_post, name='create_post'),
    path('like_post/<int:postID>', views.like_post, name='like_post'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('post_view/<int:pk>', views.post_view, name='post_view'),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post'),
    path('story', views.story, name='story'),
    path('comment/<int:pk>', views.comment, name='comment'),
    path('del_account',views.del_account, name='del_account'),

]
