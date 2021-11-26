from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('create-channel/', views.create_channel, name="create_channel"),
    path('<str:namews>_<str:id2>/dashboard', views.Dashboard, name="dashboard"),
    path('<str:namews>_<str:id2>/getdata', views.getData, name="getdata"),
    path('edit_C=<str:namews>_V=<str:id2>', views.EditVideo, name="editvideo"),
]