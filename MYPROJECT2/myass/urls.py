from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.LoginPage,name= "LoginPage"),
    path('logout/',views.LogoutUser, name= "LogoutUser"),
    path('register/',views.RegisterPage, name= "RegisterPage"),

    path('',views.home, name="home"),
    path('room/<str:pk>/',views.room, name="room"), 
    path('profile/<str:pk>/',views.userProfile, name="userProfile"),

    path('create-room/',views.createRoom, name= "createRoom"),
    path('update-room/<str:pk>/',views.UpdateRoom, name= "UpdateRoom"),
    path('delete-room/<str:pk>/',views.DeleteRoom, name= "DeleteRoom"),
    path('delete-message/<str:pk>/',views.deleteMessage, name="deleteMessage"),

    path('update-user/',views.updateUser, name= "updateUser"),

    path('topics/',views.topicPage, name= "topicPage"),
    path('activity/',views.activityPage, name= "activityPage"),
    
]
