from django.contrib import admin
from django.contrib.admin import filters
from django.contrib.admin.sites import site
from .models import Tags, channel, video, folder, Follow, comment, videoLike, videoView, dataAnalysis


class channelAdmin(admin.ModelAdmin):
    search_fields=('channel_name','phone','email')
    list_display = ('channel_name', 'owner', 'phone', 'email')

admin.site.register(channel, channelAdmin)

class folderAdmin(admin.ModelAdmin):
    search_fields=('name','channel',)
    list_display = ('name', 'channel')

admin.site.register(folder, folderAdmin)

class videoAdmin(admin.ModelAdmin):
    search_fields=('title',)
    list_filter=('date', 'channel')
    list_display = ('title', 'channel', 'date', 'total_views', 'total_likes', 'total_unlikes')

admin.site.register(video, videoAdmin)

class FollowAdmin(admin.ModelAdmin):
    search_fields=('username','channelname', 'videotitle')
    list_filter=('date','channel')
    list_display = ('username','channel', 'video', 'date')
admin.site.register(Follow, FollowAdmin)

class commentAdmin(admin.ModelAdmin):
    search_fields=('user','text', 'video')
    list_filter=('created_at',)
    list_display = ('user','text', 'videotitle', 'parent','created_at')
admin.site.register(comment, commentAdmin)

class videoLikeAdmin(admin.ModelAdmin):
    search_fields=('username','title')
    list_filter=('datetime',)
    list_display = ('title','User', 'date')
admin.site.register(videoLike, videoLikeAdmin)

class videoViewAdmin(admin.ModelAdmin):
    search_fields=('username','title')
    list_filter=('datetime',)
    list_display = ('title','User', 'date')
admin.site.register(videoView, videoViewAdmin)

class dataAnalysisAdmin(admin.ModelAdmin):
    search_fields=("channel",)
    list_display = ('channel','duration')
admin.site.register(dataAnalysis, dataAnalysisAdmin)

admin.site.register(Tags)
