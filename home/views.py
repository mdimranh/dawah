from django.http import request, response
from django.http.response import JsonResponse
from django.utils.functional import partition
from django.views.decorators.csrf import csrf_exempt
from accounts.models import CustomUser, Profile
from django.shortcuts import redirect, render
from channel.models import Tags, video, channel, folder, Follow, comment, videoLike, videoView
from django.conf import settings
from django.db.models import Count, Q
from datetime import date,datetime, timedelta
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from moviepy.editor import VideoFileClip
from django.utils import timezone
from django.utils.timezone import now
from django.contrib import messages
import random

def home(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            user_id = request.user.id
            profile = Profile.objects.get(owner = user_id)
            if profile.following.filter(id = request.POST['follow']).exists():
                Channel = channel.objects.get(id = request.POST['follow'])
                profile.following.remove(Channel)
                user = CustomUser.objects.get(id = user_id)
                Channel.follower.remove(user)
            else:
                Channel = channel.objects.get(id = request.POST['follow'])
                profile.following.add(Channel)
                user = CustomUser.objects.get(id = user_id)
                Channel.follower.add(user)
            return HttpResponseRedirect(request.path_info)
        else:
            return HttpResponseRedirect(request.path_info)
    else:
        profile = Profile.objects.filter(owner = request.user.id)
        today_video = video.objects.filter(date = date.today(), visibility = 'public')
        yesterday_video = video.objects.filter(date = date.today()-timedelta(days=1), visibility = 'public')
        thisweek_video = video.objects.filter(date__range = [date.today()-timedelta(days=7),date.today()-timedelta(days=2)], visibility = 'public')
        thismonth_video = video.objects.filter(date__range = [date.today()-timedelta(days=30),date.today()-timedelta(days=8)], visibility = 'public')
        thisyear_video = video.objects.filter(date__range = [date.today()-timedelta(days=365),date.today()-timedelta(days=31)], visibility = 'public')
        #all_video = video.objects.exclude(date = date.today()).exclude(visibility = 'private')
        no_video = 0
        no_video1 = False
        list1 = []
        if request.user.is_authenticated:
            notification_video = None
            notification_video_channel = Profile.objects.get(owner = request.user.id).following.all()
            time = Profile.objects.get(owner = request.user.id).notification_read_time
            for Channel in notification_video_channel:
                notification_video = video.objects.filter(channel = Channel, datetime__gt = time)
                for Video in notification_video:
                    list1.append(Video)
                    no_video += 1
                    no_video1 = True

        if request.user.is_authenticated:
            follow = Profile.objects.get(owner = request.user.id).following.all()
            followlist = []
            for follow in follow:
                followlist.append(follow)
        else:
            followlist = []
        current_user = request.user.id
        Channel = channel.objects.filter(owner_id = current_user)
        logo = Profile.objects.filter(owner_id = current_user)
        context = {
            'today': today_video,
            'yesterday':yesterday_video,
            'week':thisweek_video, 
            'month':thismonth_video, 
            'year':thisyear_video, 
            'channel':Channel,
            'logo':logo,
            'media_url':settings.MEDIA_URL,
            'profile':profile,
            'followlist':followlist,
            'n_video':list1,
            'no_video' : no_video,
            'no_video1' : no_video1
        }
        return render(request, 'home/index.html', context)

def Channel(request,namews, id):
    if request.method=='POST':
        if request.user.is_authenticated:
            user_id = request.user.id
            profile = Profile.objects.get(owner = user_id)
            if profile.following.filter(id = request.POST['follow']).exists():
                Channel = channel.objects.get(id = request.POST['follow'])
                profile.following.remove(Channel)
                user = CustomUser.objects.get(id = user_id)
                Channel.follower.remove(user)
            else:
                Channel = channel.objects.get(id = request.POST['follow'])
                profile.following.add(Channel)
                user = CustomUser.objects.get(id = user_id)
                Channel.follower.add(user)
            return HttpResponseRedirect(request.path_info)
        else:
            return HttpResponseRedirect(request.path_info)
    
    else:
        if request.user.is_authenticated:
            follow = Profile.objects.get(owner = request.user.id).following.all()
            followlist = []
            for follow in follow:
                followlist.append(follow)
        else:
            followlist = []
        data = channel.objects.filter(id = id)
        Video = video.objects.filter(channel_id = id, visibility = 'public')
        Folder = folder.objects.filter(channel_id = id).annotate(
            no_video=Count('video', filter=Q(video__visibility = 'public'))
        )
        current_user = request.user.id
        logo = Profile.objects.filter(owner_id = current_user)
        context = {
            'video':Video,
            'channel':data,
            'folder':Folder,
            'logo':logo,
            'media_url':settings.MEDIA_URL,
            'followlist': followlist
        }
        return render(request, 'channel/channel.html', context)

def Folder(request,channel_name, name, id):
    if request.user.is_authenticated:
        follow = Profile.objects.get(owner = request.user.id).following.all()
        followlist = []
        for follow in follow:
            followlist.append(follow)
    else:
        followlist = []
    Folder = folder.objects.filter(id = id)
    Video = video.objects.filter(folder = id, visibility = 'public')
    logo = Profile.objects.filter(owner_id = request.user.id)
    context = {
        'folder':Folder,
        'video':Video,
        'logo':logo,
        'followlist': followlist
    }
    return render(request, 'channel/folder.html',context)


@csrf_exempt
def Upload_video_save(request, channel_name, id):
    if request.method == 'POST':
        if 'title' in request.POST:
            print("im am here-------------------------------")
            Channel = channel.objects.get(id = id)
            videothumbnail = request.FILES['thumbnail']
            fsf = FileSystemStorage("media/video_thumbnail/")
            filename = fsf.save(videothumbnail.name, videothumbnail)
            videothumbnail_url = settings.MEDIA_URL+"video_thumbnail/"+filename
            videofile = request.FILES['video']
            fsv = FileSystemStorage("media/videos/")
            videoname = fsv.save(videofile.name, videofile)
            video_url = settings.MEDIA_URL+"videos/"+videoname
            duration = request.POST['duration']
            seconds = float(duration) % (24*3600)
            hour = seconds // 3600
            minutes = seconds // 60
            seconds %= 60
            if hour > 0:
                duration = "%d:%02d:%02d" % (hour, minutes, seconds)
            elif hour == 0 and minutes > 0:
                duration = "%02d:%02d" % (minutes, seconds)
            else:
                duration = "%02d s" % (seconds)

            Video = video(
                channel = Channel,
                title = request.POST['title'],
                thumbnail = videothumbnail_url,
                description = request.POST['description'],
                tag = request.POST['tag'],
                video = video_url,
                duration = duration,
                visibility = request.POST['visibility']
            )

            all_video = video.objects.all()
            videolist = []
            for allvideo in all_video:
                videolist.append(allvideo.id2)

            print(videolist)

            a1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            a2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            a3 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            a4 = [a1, a2, a3]
            id2 = ''
            loop = True
            while loop:
                for i in range(12):
                    id2 += random.choice(random.choice(a4))
                if id2 in videolist:
                    continue
                else:
                    Video.id2 = id2
                    break

            # vfile = ('G:/Project/dawah1/'+video_url)
            # video_file = VideoFileClip(vfile)
            # duration = video_file.duration
            # seconds = duration % (24*3600)
            # hour = seconds // 3600
            # minutes = seconds // 60
            # seconds %= 60
            # if hour > 0:
            #     Video.duration = "%d:%02d:%02d" % (hour, minutes, seconds)
            # elif hour == 0 and minutes > 0:
            #     Video.duration = "%02d:%02d" % (minutes, seconds)
            # else:
            #     Video.duration = "%02d s" % (seconds)
            Video.save()

            getsavedvideo = video.objects.get(id2 = id2)

            if request.POST['folder'] == '':
                Folder = None
            else:
                flist = (request.POST['folder']).split(",")
                for fl in flist:
                    Folder = folder.objects.get(id = fl)
                    getsavedvideo.folder.add(Folder)
            getsavedvideo.save()
            for tag in getsavedvideo.tag.split(" ,"):
                tag, create = Tags.objects.get_or_create(name = tag)
                tag.video.add(getsavedvideo)
                tag.save()
            print("Saved-------------------------------")
            return HttpResponse('Success')
        
        elif 'folder_name' in request.POST:
            thumbnail = request.FILES['folderthumbnail']
            fs = FileSystemStorage("media/thumbnail/")
            filename = fs.save(thumbnail.name, thumbnail)
            thumbnail_url = settings.MEDIA_URL+"thumbnail/"+filename
            Folder = folder(
                name = request.POST['folder_name'],
                thumbnail = thumbnail_url,
                channel_id = id
            )
            Folder.save()
            return HttpResponse("Successfull")
        elif 'notification' in request.POST:
            profile = Profile.objects.get(owner = request.user)
            profile.notification_read_time = datetime.now()
            profile.save()
            return HttpResponse("Success")
    else:
        return HttpResponse("Successfull")

from django.utils.datastructures import MultiValueDictKeyError
@csrf_exempt
def Edit_video_save(request, channel_name, id):
    if request.method == 'POST':
        print("I am in video update section...")
        if 'title' in request.POST:
            Video = video.objects.get(id2 = request.POST['id2'])
            try:
                videothumbnail = request.FILES['thumbnail']
                fsf = FileSystemStorage("media/video_thumbnail/")
                filename = fsf.save(videothumbnail.name, videothumbnail)
                videothumbnail_url = settings.MEDIA_URL+"video_thumbnail/"+filename
                Video.thumbnail = videothumbnail_url
            except MultiValueDictKeyError:
                pass

            Video.title = request.POST['title']
            Video.description = request.POST['description']
            Video.visibility = request.POST['visibility']

            if request.POST['folder'] == '':
                Folder = None
            else:
                flist = (request.POST['folder']).split(",")
                for fl in flist:
                    Folder = folder.objects.get(id = fl)
                    Video.folder.add(Folder)
            Video.save()
            print("Video updated successfully...")
            return HttpResponse('Success')
    else:
        return HttpResponse("Successfull")


def createfolder(request, channel_name, id):
    Folder = folder.objects.filter(channel_id = id)
    context = {
        "folder" : list(Folder.values())
    }
    return JsonResponse(context)


def time_format(timeduration):
    c = 0
    tm = ""
    for i in timeduration:
        if i != ":" and i != ",":
            tm += i
        elif i == ",":
            t = tm.split(" ")
            if int(t[0]) >= 7 and int(t[0]) < 30:
                i = int(t[0])//7
                if i == 1:
                    i = str(i)+" week ago"
                else:
                    i = str(i)+" weeks ago"
                tm = i
            elif int(t[0]) >= 31 and int(t[0]) < 366:
                i = int(t[0])//30
                if i == 1:
                    i = str(i)+" month ago"
                else:
                    i = str(i)+ " months ago"
                tm = i
            elif int(t[0]) >= 365:
                i = int(t[0])//365
                if i == 1:
                    i = str(i)+" year ago"
                else:
                    i = str(i)+ " years ago"
                tm = i
            else:
                i = " ago"
                tm += i
            break
        elif i == ":" and c == 0:
            if tm != "0":
                if tm != "1":
                    i = " hours ago"
                else:
                    i = "hour ago"
                tm += i
                c = 1
                break
            else:
                tm = ""
                c = 1
        elif i == ":" and c == 1:
            tm = int(tm)
            tm = str(tm)
            if tm == "0":
                tm = "Now"
                break
            if tm == "1":
                i = " minute ago"
                tm += i
                break
            else:
                i = " minutes ago"
                tm += i
                break
    return tm

def getNotification(request):
    notification_video_channel = Profile.objects.get(owner = request.user.id).following.all()
    time = Profile.objects.get(owner = request.user.id).notification_read_time
    list1 = []
    channellist = []
    namewslist = []
    logolist = []
    n_video_timelist = []
    userlist = []
    comment_timelist = []
    no_video = video.objects.filter(channel__in = notification_video_channel, datetime__gt = time, visibility = 'public').count()
    notification_video1 = video.objects.filter(channel__in = notification_video_channel)
    for Video in notification_video1:
        list1.append(Video.id)
    getvideo = video.objects.filter(id__in = list1, visibility = 'public').order_by('datetime')
    if channel.objects.filter(owner = request.user).exists():
        getchannel = channel.objects.get(owner = request.user)
        getcomment = comment.objects.filter(video__channel = getchannel).order_by('created_at')
        no_comment = comment.objects.filter(video__channel = getchannel, created_at__gt = time).count()
    else:
        getcomment = comment.objects.filter(parent__user = request.user).order_by('created_at')
        no_comment = comment.objects.filter(parent__user = request.user, created_at__gt = time).count()
    for v in getvideo:
        channellist.append(v.channel.channel_name)
        namewslist.append(v.channel.namews)
        logolist.append(v.channel.logo)
        timeduration = str(now() - v.datetime)
        n_video_timelist.append(time_format(timeduration))
    profilelist = []
    comment_video_thumbnail = []
    for c in getcomment:
        userlist.append(c.user.fullname)
        timeduration = str(now() - c.created_at)
        comment_timelist.append(time_format(timeduration))
        getprofile = Profile.objects.get(owner = c.user)
        profilelist.append(getprofile.image)
        comment_video_thumbnail.append(c.video.thumbnail)

    no_notification = no_video+no_comment
        
    context = {
        "n_video" : list(getvideo.values()),
        'n_video_timelist' : n_video_timelist,
        "comment" : list(getcomment.values()),
        'no_video': no_video,
        'no_comment': no_comment,
        'no_notification': no_notification,
        'channellist': channellist,
        'namewslist': namewslist,
        'logolist': logolist,
        'userlist': userlist,
        'comment_timelist': comment_timelist,
        'profilelist': profilelist,
        'cv_thumbnail': comment_video_thumbnail
    }
    return JsonResponse(context)

def Upload_video(request, channel_name, id):
    if request.user.is_authenticated:
        follow = Profile.objects.get(owner = request.user.id).following.all()
        followlist = []
        for follow in follow:
            followlist.append(follow)
    else:
        followlist = []
    current_user = request.user.id
    Channel = channel.objects.filter(owner = current_user)
    Folder = folder.objects.filter(channel_id = id)
    logo = Profile.objects.filter(owner_id = request.user.id)


    no_video = 0
    no_video1 = False
    if request.user.is_authenticated:
        notification_video = None
        notification_video_channel = Profile.objects.get(owner = request.user.id).following.all()
        time = Profile.objects.get(owner = request.user.id).notification_read_time
        for i in notification_video_channel:
            notification_video = video.objects.filter(channel = i, datetime__gt = time)
            for Video in notification_video:
                no_video += 1
                no_video1 = True


    context = {
        'folder':Folder,
        'channel':Channel,
        'logo':logo,
        'followlist' : followlist,
        'no_video' : no_video,
        'no_video1' : no_video1
    }
    return render(request, 'video/upload_video.html', context)

def createComment(request,namews, id2):
    if request.method == 'POST':
        Comment = request.POST['comment']
        parentid = request.POST['parentid']
        Video = video.objects.get(id2 = id2)
        if parentid:
            parent = comment.objects.get(id=parentid)
            newcom = comment(video = Video, text = Comment, parent = parentid, user = request.user)
            newcom.save()
        else:
            newcom = comment(video = Video, text = Comment, user = request.user)
            newcom.save()

@csrf_exempt
def play(request,namews, id2):
    if request.method=='POST':
        if request.user.id:
            user_id = request.user.id
            if 'follow' in request.POST:
                profile = Profile.objects.get(owner = user_id)
                if profile.following.filter(id = request.POST['follow']).exists():
                    Channel = channel.objects.get(id = request.POST['follow'])
                    profile.following.remove(Channel)
                    user = CustomUser.objects.get(id = user_id)
                    Channel.follower.remove(user)
                    Video = video.objects.get(id2 = id2)
                    Follow.objects.filter(video = Video).delete()
                else:
                    Channel = channel.objects.get(id = request.POST['follow'])
                    profile.following.add(Channel)
                    user = CustomUser.objects.get(id = user_id)
                    Channel.follower.add(user)
                    Video = video.objects.get(id2 = id2)
                    follow = Follow(
                        user = request.user,
                        channel = Channel,
                        video = Video
                    )
                    follow.save()
                return HttpResponse("Success")
            elif 'like' in request.POST:
                Video = video.objects.get(id2 = id2)
                user = CustomUser.objects.get(id = user_id)
                if Video.likes.filter(id = user_id).exists():
                    videoLike.objects.filter(user = user, video = Video).delete()
                    Video.likes.remove(user)
                else:
                    if Video.unlikes.filter(id = user_id).exists():
                        Video.unlikes.remove(user)
                    Video.likes.add(user)
                    addlike = videoLike(
                        user = user,
                        title = Video.title[0: 30]+"...",
                        username = user.fullname,
                        channel = Video.channel,
                        video = Video
                    )
                    addlike.save()
                return HttpResponse('Successfull')
            elif 'unlike' in request.POST:
                Video = video.objects.get(id2 = id2)
                user = CustomUser.objects.get(id = user_id)
                if Video.unlikes.filter(id = user_id).exists():
                    Video.unlikes.remove(user)
                else:
                    Video.unlikes.add(user)
                    if Video.likes.filter(id = user_id).exists():
                        Video.likes.remove(user)
                        videoLike.objects.filter(user = user, video = Video).delete()
                return HttpResponse(request.path_info)
            elif 'comment' in request.POST:
                Comment = request.POST['comment']
                parentid = request.POST['parentid']
                Video = video.objects.get(id2 = id2)
                if parentid:
                    parent = comment.objects.get(id=parentid)
                    newcom = comment(video = Video, text = Comment, parent = parentid, user = request.user)
                    newcom.save()
                else:
                    newcom = comment(video = Video, text = Comment, user = request.user)
                    newcom.save()
                return HttpResponse("Add comment successfull...")
            elif 'love' in request.POST:
                getcomment = comment.objects.get(id = request.POST['love'])
                if getcomment.love.filter(id = request.user.id).exists():
                    getcomment.love.remove(request.user)
                else:
                    getcomment.love.add(request.user)
                return HttpResponse("Successfull")
        else:
            messages.info(request, 'Three credits remain in your account.')
    else:
        if request.user.is_authenticated:
            follow = Profile.objects.get(owner = request.user.id).following.all()
            followlist = []
            for follow in follow:
                followlist.append(follow)
        else:
            followlist = []
        logo = Profile.objects.filter(owner_id = request.user.id)
        Channel = channel.objects.filter(owner = request.user.id)
        Video = video.objects.filter(id2 = id2)
        data = video.objects.get(id2 = id2)
        if request.user.id:
            if data.views.filter(id = request.user.id).exists():
                pass
            else:
                data.views.add(request.user)
                addview = videoView(
                    user = request.user,
                    title = data.title[0: 30]+"...",
                    username = request.user.fullname,
                    channel = data.channel,
                    video = data
                )
                addview.save()

        total_likes = data.likes.all().count()
        total_unlikes = data.unlikes.all().count()
        try:
            percentage = total_likes*int(100//(total_likes+total_unlikes))
        except ZeroDivisionError:
            percentage = 0
        follow = False
        like = False
        unlike = False
        if request.user.id:
            profile = Profile.objects.get(owner = request.user.id)
            if profile.following.filter(id = data.channel.id).exists():
                follow = True
            if videoLike.objects.filter(user = request.user, video = data).exists():
                like = True
                unlike = False
            elif data.unlikes.filter(id = request.user.id).exists():
                like = False
                unlike = True
        related_video = video.objects.all().exclude(id2 = id2)


        no_video = 0
        no_video1 = False
        if request.user.is_authenticated:
            notification_video = None
            notification_video_channel = Profile.objects.get(owner = request.user.id).following.all()
            time = Profile.objects.get(owner = request.user.id).notification_read_time
            for i in notification_video_channel:
                notification_video = video.objects.filter(channel = i, datetime__gt = time)
                for x in notification_video:
                    no_video += 1
                    no_video1 = True

        context = {
            'channel':Channel,
            'video': Video,
            'related_video': related_video,
            'logo': logo,
            'follow': follow,
            'like': like,
            'total_like': total_likes,
            'unlike' : unlike,
            'percentage': [percentage],
            'followlist': followlist,
            'media_url':settings.MEDIA_URL,
            'no_video' : no_video,
            'no_video1' : no_video1
        }
        return render(request, 'play/play.html', context)


def getVideoDetails(request, namews, id2):
    Video = video.objects.filter(id2 = id2)
    data = video.objects.get(id2 = id2)
    if request.user.id:
        data.views.add(request.user)
    total_likes = int(videoLike.objects.filter(video = data).count())
    total_unlikes = data.unlikes.all().count()
    try:
        percentage = total_likes*int(100//(total_likes+total_unlikes))
    except ZeroDivisionError:
        percentage = 0
    like = False
    unlike = False
    if request.user.id:
        profile = Profile.objects.get(owner = request.user.id)
        if videoLike.objects.filter(user = request.user, video = data).exists():
            like = True
            unlike = False
        elif data.unlikes.filter(id = request.user.id).exists():
            like = False
            unlike = True
    comments = comment.objects.filter(video = data, replay = 'no').order_by("-created_at")
    replay = comment.objects.filter(video = data, replay = 'yes')
    namelist = []
    replay_namelist = []
    logolist = []
    replay_logolist = []
    comment_total_love = []
    replay_total_love = []
    parentid = []
    for x in comments:
        timeduration = str(now() - x.created_at)
        td = time_format(timeduration)
        namelist.append((x.user.fullname, td))
        logo = Profile.objects.get(owner = x.user.id)
        logolist.append(logo.image)
        comment_total_love.append(x.love.count())
    for r in replay:
        timeduration = str(now() - r.created_at)
        td = time_format(timeduration)
        replay_namelist.append((r.user.fullname, td))
        logo = Profile.objects.get(owner = r.user.id)
        replay_logolist.append(logo.image)
        replay_total_love.append(r.love.count())
        parentid.append(r.parent.id)

    if request.user in data.channel.follower.all():
        follow = True
    else:
        follow = False
    total_follower = data.channel.follower.all().count()
    context = {
        "total_likes" : total_likes,
        "total_unlikes" : total_unlikes,
        'total_follower' : total_follower,
        "like":like,
        'unlike': unlike,
        "percentage": percentage,
        'follow': follow,
        "comment": list(comments.values()),
        "parentid": parentid,
        "replay": list(replay.values()),
        "comment_total_love": comment_total_love,
        "replay_total_love": replay_total_love,
        'name': namelist,
        'replay_name': replay_namelist,
        'logo': logolist,
        'replay_logo': replay_logolist,
    }
    return JsonResponse(context)


@csrf_exempt
def Search(request, value):
    val = value.replace('+', ' ')
    rslt = searchReuslt(val)
    result = video.objects.filter(title__in = rslt)
    context={
        "video": result,
        "value": val
    }
    return render(request, 'home/search.html', context)

import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def searchReuslt(value):
    model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
    df = pd.read_excel('G:\Project\dawah1\media\searchdata.xlsx')

    def find_similar(vector_representation, all_representations, k=1):
        similarity_matrix = cosine_similarity(vector_representation, all_representations)
        np.fill_diagonal(similarity_matrix, 0)
        similarities = similarity_matrix[0]
        if k == 1:
            return [np.argmax(similarities)]
        elif k is not None:
            return np.flip(similarities.argsort()[-k:][::1])

    paragraph = df.iloc[:, 0] # the first column values
    embeddings_distilbert = model.encode(paragraph.values)
    search_string = value
    search_vect = model.encode([search_string])
    distilbert_similar_indexes = find_similar(search_vect, embeddings_distilbert)
    output_data = []
    for index in distilbert_similar_indexes:
        output_data.append(paragraph[index])

    import openpyxl
    file = (r'G:\Project\dawah1\media\searchdata.xlsx')
    wb = openpyxl.load_workbook(filename=file)
    rs = video.objects.all()
    sheet = wb['Sheet1']
    from googletrans import Translator
    for Video in rs:
        translator = Translator()
        translation = translator.translate(Video.title)
        new_row = [translation.text]
        sheet.append(new_row)
    wb.save(file)

    return output_data


def Tag(request, tag):
    Video = Tags.objects.get(name = tag)
    return render(request, 'home/search.html', {'video': Video, 'tag': True})