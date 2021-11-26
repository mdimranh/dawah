from django.db.models.expressions import F
from django.http.response import HttpResponse, JsonResponse
from accounts.views import profile
from django.shortcuts import redirect, render
from .models import Follow, channel, comment, dataAnalysis, video, folder, videoView, videoLike
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from accounts.models import Profile
import random
from datetime import date, datetime,timedelta
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt

def create_channel(request):

    current_user = request.user

    if request.method == 'POST':
        logo = Profile.objects.get(owner = current_user)
        fname = ""
        lname = ""
        for name in request.user.first_name:
            if name != " ":
                fname += name
        for name in request.user.last_name:
            if name != " ":
                lname += name
        Channel = channel(
            owner_id = current_user.id,
            #channel_name = current_user.first_name +' '+ current_user.last_name,
            namews = fname+lname,
            logo = logo.image,
            phone = request.POST['phoneNumber'],
            email = request.POST['email'],
            about_allah = request.POST['aboutAllah'],
            fb_link = request.POST['fb_link'],
            twitter_link = request.POST['twitter_link'],
            web_link = request.POST['web_link']
        )
        all_channel = channel.objects.all()
        channellist = []
        for allchannel in all_channel:
            channellist.append(allchannel.id2)
        a1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        a2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        a3 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        a4 = [a1, a2, a3]
        id2 = ''
        loop = True
        while loop:
            for i in range(12):
                id2 += random.choice(random.choice(a4))
            if id2 in channellist:
                continue
            else:
                Channel.id2 = id2
                break
        Channel.save()
        return redirect('/')

    else:
        return render(request, 'channel/index.html')


@csrf_exempt
def Dashboard(request, namews, id2):

    if request.method == 'POST':
        if 'duration' in request.POST:
            Channel = channel.objects.get(id2 = id2)
            if dataAnalysis.objects.filter(channel = Channel).exists():
                da = dataAnalysis.objects.get(channel = Channel)
                da.duration = request.POST['duration']
                da.save()
            else:
                da = dataAnalysis(
                    channel = channel.objects.get(id2 = id2),
                    duration = request.POST['duration']
                )
                da.save()
            return HttpResponse("Success")
        else:
            return HttpResponse("Success")

    else:
        Channel = channel.objects.filter(id2 = id2)
        getchannel = channel.objects.get(id2 = id2)
        logo = Profile.objects.filter(owner_id = request.user)
        no_video = 0
        no_video1 = False
        if request.user.is_authenticated:
            notification_video = None
            notification_video_channel = Profile.objects.get(owner = request.user.id).following.all()
            time = Profile.objects.get(owner = request.user.id).notification_read_time
            list1 = []
            for Channel1 in notification_video_channel:
                notification_video = video.objects.filter(channel = Channel1, datetime__gt = time)
                for Video in notification_video:
                    list1.append(Video.id)
                    no_video += 1
                    no_video1 = True
        allvideo = video.objects.filter(channel = getchannel).order_by('datetime')
        totalvideo = video.objects.filter(channel = getchannel).count()
        follower = getchannel.total_follower
        Folder = folder.objects.filter(channel = getchannel).count()
        Folders = folder.objects.filter(channel_id = getchannel.id).annotate( no_video=Count('video'))
        total_comments = []
        for vdio in allvideo:
            total_comment = comment.objects.filter(video = vdio).count()
            total_comments.append(total_comment)

        from datetime import date
        no_view = []
        no_like = []
        day_name = []
        day_date = []
        for d in range(7):
            views = videoView.objects.filter(channel = getchannel, date = ((date.today()-timedelta(days=d)).strftime("%Y-%m-%d"))).count()
            no_view.append(views)
            day = (date.today()-timedelta(days=d)).strftime("%a")
            day_name.append(day)
            likes = videoLike.objects.filter(channel = getchannel, date = ((date.today()-timedelta(days=d)).strftime("%Y-%m-%d"))).count()
            no_like.append(likes)
        no_view.reverse()
        no_like.reverse()
        day_name.reverse()
        day_date.reverse()
        totalview = 0
        totallike = 0
        for view in no_view:
            totalview+=view
        for like in no_like:
            totallike+=like

        from datetime import date
        today = date.today()
        todaylikes = videoLike.objects.filter(channel =  getchannel,date = today).count()
        todayviews = videoView.objects.filter(channel =  getchannel, date = today).count()
        comments = comment.objects.filter(date = today)
        todaycomments = 0
        for c in comments:
            if c.video.channel == getchannel:
                todaycomments += 1
        todayfollow = Follow.objects.filter(channel =  getchannel, date = today).count()
        todaydata = [todayviews, todaylikes, todaycomments, todayfollow]

        last_video = video.objects.filter(channel = getchannel).order_by('-datetime')[:1]
        last_video_view = videoView.objects.filter(video = last_video).count()
        last_video_like = videoLike.objects.filter(video = last_video).count()

        topvideo = []
        myvideo = video.objects.filter(channel = getchannel).order_by('-datetime')
        for mv in myvideo[:5]:
            try:
                percentage = mv.likes.count()*int(100//(mv.likes.count()+mv.unlikes.count()))
            except ZeroDivisionError:
                percentage = 0
            topvideo.append((mv, percentage+mv.views.count()))
        topvideo.sort(key= lambda x: x[1], reverse=True)
        print(topvideo)

        context = {
            'channel' : Channel,
            'logo':logo,
            'no_video': no_video,
            'no_video1': no_video1,
            'video': allvideo,
            'totalvideo': totalvideo,
            'comments': total_comments,
            'follower' : follower,
            'folder': Folder,
            'folders': Folders,
            'no_view': no_view,
            'no_like': no_like,
            'totalview':totalview,
            'totallike':totallike,
            'day_name': day_name,
            'todaydata': todaydata,
            'topvideo': topvideo,
            'number': [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000],
            'sidebar': True
        }
        return render(request, 'channel/dashboard.html', context)


def EditVideo(request, namews, id2):
    Video = video.objects.get(id2 = id2)
    Folder = folder.objects.filter(channel = Video.channel)
    if request.user.is_authenticated:
        follow = Profile.objects.get(owner = request.user.id).following.all()
        followlist = []
        for follow in follow:
            followlist.append(follow)
    else:
        followlist = []
    current_user = request.user.id
    Channel = channel.objects.filter(owner = current_user)
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
        'no_video1' : no_video1,
        'video': Video
    }
    return render(request, 'video/edit_video.html', context)


def getData(request, namews, id2):
    getchannel = channel.objects.get(id2 = id2)
    from datetime import date
    no_view = []
    no_like = []
    day_name = []
    day_date = []
    Duration = int(dataAnalysis.objects.get(channel = getchannel).duration)
    if Duration < 365:
        for d in range(Duration):
            views = videoView.objects.filter(channel = getchannel, date = ((date.today()-timedelta(days=d)).strftime("%Y-%m-%d"))).count()
            no_view.append(views)
            if Duration == 7 :
                day = (date.today()-timedelta(days=d)).strftime("%a")
            if Duration == 30:
                day = (date.today()-timedelta(days=d)).strftime("%b-%d")
            day_name.append(day)
            likes = videoLike.objects.filter(channel = getchannel, date = ((date.today()-timedelta(days=d)).strftime("%Y-%m-%d"))).count()
            no_like.append(likes)
    else:
        today = date.today()
        month = int(today.strftime("%m"))
        year = int(today.strftime("%Y"))
        y = int(today.strftime("%y"))
        monthName = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for m in range(12):
            if int(month) == 12:
                views = videoView.objects.filter(channel = getchannel, date__month=month, date__year=year).count()
                likes = videoLike.objects.filter(channel = getchannel, date__month=month, date__year=year).count()
                no_view.append(views)
                no_like.append(likes)
                year -= 1
                y -= 1
                day_name.append(f"{monthName[month-1]}-{y}")
                month -= 1
                if month == 0:
                    month = 12
            else:
                views = videoView.objects.filter(channel = getchannel, date__month=month, date__year=year).count()
                likes = videoLike.objects.filter(channel = getchannel, date__month=month, date__year=year).count()
                no_view.append(views)
                no_like.append(likes)
                day_name.append(f"{monthName[month-1]}-{y}")
                month -= 1
                if month == 0:
                    month = 12

    no_view.reverse()
    no_like.reverse()
    day_name.reverse()
    day_date.reverse()
    totalview = 0
    totallike = 0
    for view in no_view:
        totalview+=view
    for like in no_like:
        totallike+=like

    context = {
        'no_view': no_view,
        'no_like': no_like,
        'totalview':totalview,
        'totallike':totallike,
        'day_name': day_name,
        'duration': Duration
    }
    return JsonResponse(context)

