from django.contrib.auth.models import User
from django.urls import path
from . import views
from django.contrib.auth.models import User, auth



urlpatterns = [
    path('login/', views.login, name="login"),
    path('profile/', views.profile, name="profile"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('profile_update', views.profileUpdate, name="profileUpdate"),
]