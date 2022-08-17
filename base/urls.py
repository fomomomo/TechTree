from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('all-polls/', views.allPolls, name='all-polls'),

    path('poll/<str:pk>/', views.poll, name="poll"),
    path('create-poll/<str:pk>/', views.createPoll, name="create-poll"),
    path('create-option/<str:pk>/', views.createOption, name="create-option"),

    path('vote/<str:pk>/', views.votePage, name='vote'),
    path('voted-already/<str:pk>/', views.votedAlready, name='voted-already'),

]
