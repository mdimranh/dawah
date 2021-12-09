from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('play_C=<str:namews>_V=<str:id2>', views.play, name="play"),
    path('play_C=<str:namews>_V=<str:id2>/getvideodetails', views.getVideoDetails, name="getvideodetails"),
    path('getnotifications', views.getNotification, name="getnotifications"),
    path('notificationseen/<int:id>', views.notificationseen, name="notificationseen"),
    path('channel/<str:namews>_<int:id>', views.Channel, name="channel"),
    path('play_C=<str:namews>_V=<str:id2>/createcomment', views.createComment, name="createcomment"),
    path('channel/<str:channel_name>/<int:id>/upload-video', views.Upload_video, name="upload_video"),
    path('<int:id>/delete-video', views.Delete_video, name="delete_video"),
    path('channel/<str:channel_name>/<int:id>/upload-video-save', views.Upload_video_save, name="upload_video_save"),
    path('channel/<str:channel_name>/<int:id>/edit-video-save', views.Edit_video_save, name="edit_video_save"),
    path('channel/<str:channel_name>/<int:id>/createfolder', views.createfolder, name="create_folder"),
    path('channel/<str:namews>/<str:name>_<int:id>', views.Folder, name="folder"),
    path('search/<str:value>', views.Search, name="search"),
    path('t_<str:tag>', views.Tag, name="tag"),
]