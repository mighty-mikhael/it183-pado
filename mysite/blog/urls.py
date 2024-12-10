from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import blog_details
from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
    LikeDislikeCreateView
)

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.blog_list, name='blog_list'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.update_post, name='update_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('about/', views.about, name='about'),
    path('details/<int:pk>/', blog_details, name='blog_details'),
    #API

    path('api/posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('api/posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post_detail'),

    # Likes/Dislikes
    path('api/posts/<int:post_id>/like_dislike/', LikeDislikeCreateView.as_view(), name='like_dislike_create'),
]