"""Instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Insta.views import PostsView, PostDetailView, PostCreateView, \
    PostUpdateView, PostDeleteView, addLike, UserDetailView, addComment, \
    EditProfile, toggleFollow, ExploreView, UsersView, FollowedView, FollowingView, CommentDeleteView, \
    PicUpdateView, WelcomeView

urlpatterns = [
    path('posts/', PostsView.as_view(), name = 'posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post_detail'),
    path('post/create/', PostCreateView.as_view(), name = 'post_create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name = 'post_update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name = 'post_delete'),
    path('like', addLike, name='addLike'),
    path('user/<int:pk>/', UserDetailView.as_view(), name = 'user_detail'),
    path('comment', addComment, name='addComment'),
    path('edit_profile/<int:pk>/', EditProfile.as_view(), name='edit_profile'),
    path('togglefollow', toggleFollow, name='togglefollow'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('users/', UsersView.as_view(), name='users_view'),
    path('following/<int:pk>/', FollowingView.as_view(), name='following_view'),
    path('followed/<int:pk>/', FollowedView.as_view(), name='followed_view'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name = 'comment_delete'),
    path('pic_update/<int:pk>/', PicUpdateView.as_view(), name='pic_update'),
    path('welcome/', WelcomeView.as_view(), name='welcome_view')
]