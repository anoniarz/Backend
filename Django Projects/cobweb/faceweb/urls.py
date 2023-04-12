from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='faceweb_home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.delete_post, name='post-delete'),
    path('about/', views.about, name='blog-about'),
    


    path('chat', views.index, name="index"),
    path('friend/<str:pk>', views.detail, name="detail"),
    path('sent_msg/<str:pk>', views.sentMessages, name = "sent_msg"),
    path('rec_msg/<str:pk>', views.receivedMessages, name = "rec_msg"),
    path('notification', views.chatNotification, name = "notification"),
]
