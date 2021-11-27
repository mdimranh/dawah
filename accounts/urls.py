from django.contrib.auth.models import User
from django.urls import path
from . import views
from django.contrib.auth.models import User, auth



urlpatterns = [
    path('login/', views.login, name="login"),
    path('profile/', views.profile, name="profile"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('verify/<str:activation_key>', views.email_confirm, name='email_confirm'),
    path('password_recover/<str:activation_key>', views.password_recover, name='password_recover'),
    path('profile_update', views.profileUpdate, name="profileUpdate"),
]