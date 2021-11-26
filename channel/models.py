from django.db import models
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey
from django.forms import forms
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings

from django.utils.timezone import now

class channel(models.Model):
    id2 = TextField(default='', unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    namews = models.CharField(max_length=255)
    logo = models.TextField()
    phone = models.IntegerField()
    email = models.CharField(max_length=100)
    about_allah = models.TextField()
    fb_link = models.TextField()
    twitter_link = models.TextField()
    web_link = models.TextField()
    date = models.DateField(default=now)
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Follower', default=None, blank=True)
    @property
    def channel_name(self):
        return self.owner.fullname

    def total_follower(self):
        return self.follower.count()

    def __str__(self):
        return self.channel_name

class folder(models.Model):
    channel = models.ForeignKey(channel, on_delete=models.CASCADE)
    name = models.TextField()
    thumbnail = models.URLField()

    def __str__(self):
        return self.name

class video(models.Model):
    VISIBILITY = (
        ('public', 'public'),
        ('private', 'private'),
    )
    id2 = TextField(default='')
    channel = models.ForeignKey(channel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    thumbnail = models.CharField(default='/media/thumbnail/image.jpg', max_length=500)
    folder = models.ManyToManyField(folder, default=None, blank=True)
    tag = models.TextField(default="", null=True, blank=True)
    description = models.TextField()
    video = models.CharField(null=True, max_length=500)
    duration = models.TextField(null=True)
    visibility = models.CharField(max_length=100,default='public', choices=VISIBILITY)
    date = models.DateField(default=now)
    datetime = models.DateTimeField(default=now)
    views = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Views', default=None, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', default=None, blank=True)
    unlikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Unlikes', default=None, blank=True)
    shares = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Shares', default=None, blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Bookmarks', default=None, blank=True)

    def tags(self):
        tg = self.tag.split(' ,')
        return tg

    def total_views(self):
        return self.views.count()

    def total_likes(self):
        return self.likes.count()

    def total_unlikes(self):
        return self.unlikes.count()

    def total_shares(self):
        return self.shares.count()

    def total_bookmarks(self):
        return self.bookmarks.count()

    def titles(self):
        if len(self.title) > 50:
            return self.title[0:50]+"..."
        else:
            return self.title

    def __str__(self):
        return self.title


class Follow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    channel = models.ForeignKey(channel, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    video = models.ForeignKey(video, on_delete=models.CASCADE)

    def username(self):
        return self.user.fullname

    def channelname(self):
        return self.channel.channel_name

    def videotitle(self):
        return self.video.title

class videoLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    video = models.ForeignKey(video, on_delete=models.CASCADE)
    channel = models.ForeignKey(channel, on_delete=models.CASCADE,blank=True, null=True)
    title = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=100, null=True)
    datetime = models.DateTimeField(default=now)
    date = models.DateField(default=now)

    def User(self):
        return self.username

class videoView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    video = models.ForeignKey(video, on_delete=models.CASCADE)
    channel = models.ForeignKey(channel, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=100, null=True)
    datetime = models.DateTimeField(default=now)
    date = models.DateField(default=now)

    def __str__(self):
        return self.video.title

    def User(self):
        return self.username


class comment(models.Model):
    REPLAY = (
        ('yes', "yes"),
        ('no', "no"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(video, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    replay = models.CharField(max_length=100,default='no', choices=REPLAY)
    created_at = models.DateTimeField(default=now)
    date = models.DateField(default=now)
    love = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='loves', default=None, blank=True)

    def __str__(self):
        return self.text[0:25]+"..."

    def names(self):
        return self.user.fullname

    def sorttext(self):
        return self.text[0:30]+"..."

    def channel(self):
        return self.video.channel

    def videotitle(self):
        return self.video.title[0:25]+"..."

    def total_love(self):
        return self.love.count()

class dataAnalysis(models.Model):
    channel = models.ForeignKey(channel, on_delete=models.CASCADE)
    duration = models.CharField(max_length=50, default=7)

    def __str__(self):
        return self.channel.channel_name
