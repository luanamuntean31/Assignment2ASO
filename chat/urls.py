from django.contrib.messages import success
from django.urls import path
from . import views

from django.conf.urls import url, include
from django.contrib import admin

from .views import PostImage, PostImageDisplay

urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),

	path('<str:room>/', views.room, name='room'),
	path('checkview', views.checkview, name='checkview'),
	path('send', views.send, name='send'),
	path('getMessages/<str:room>/', views.getMessages, name='getMessages'),

    #path('', PostImage.as_view(), name='posts'),
    #path('posts/', views.posts, name='posts'),
    #path('post-image/<int:pk>/', PostImageDisplay.as_view(), name='post_image_display'),

	path('image_upload', PostImage.as_view(), name='image_upload'),
	#path('success', success, name='success'),
	path('post-image/<int:pk>/', PostImageDisplay.as_view(), name='post_image_display')

]