from django.contrib.auth import models
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from channel.models import channel, video
from .models import CustomUser, Profile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@csrf_exempt
def signup(request):
    if request.method == 'POST' and request.FILES['image']:
        if 'first_name' in request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            Phone = request.POST['phone']
            password = request.POST['password']

            if User.objects.filter(phone=Phone).exists():
                messages.info(request,'This phone is already exist.')
                return redirect('signup')
            else:
                user = User.objects.create_user(phone=Phone, password=password, first_name=first_name,
                                                last_name=last_name)
                user.save()

                image = request.FILES['image']
                fs = FileSystemStorage("media/logo/")
                filename = fs.save(image.name, image)
                image_url = settings.MEDIA_URL+"logo/"+filename
                Owner = CustomUser.objects.get(phone = Phone)
                profile = Profile(
                    owner = Owner,
                    image = image_url,
                )
                profile.save()

                messages.info(request, 'successfull')
                return redirect('login')
        
        if 'new_first_name' in request.POST:
            getuser = CustomUser.objects.get(id = request.user.id)
            getuser.first_name = request.POST['new_first_name']
            getuser.last_name = request.POST['new_last_name']
            getuser.phone = request.POST['new_phone']
            getuser.save()
            getprofile = Profile.objects.get(owner = request.user)
            image = request.FILES['new_logo']
            fs = FileSystemStorage("media/logo/")
            filename = fs.save(image.name, image)
            image_url = settings.MEDIA_URL+"logo/"+filename
            getprofile.image = image_url
            getprofile.save()
            Video = video.objects.all()
            likes = 0
            views = 0
            for Video in Video:
                if Video.likes.filter(id = request.user.id).exists():
                    likes += 1
                if Video.views.filter(id = request.user.id).exists():
                    views += 1
                    
                current_user = request.user.id
                Channel = channel.objects.filter(owner = current_user)
                Channel_no = channel.objects.filter(owner = current_user).count()
                logo = Profile.objects.filter(owner_id = current_user)
                context = {
                    "channel":Channel,
                    "no_channel":Channel_no,
                    'logo': logo,
                    'likes': likes,
                    'views': views,
                }
                return render(request, 'profile/profile.html', context)
    else:
        return render(request, 'account/signup.html')


@csrf_exempt
def profileUpdate(request):
    if request.method == 'POST':
        print("get data and update")
        getuser = CustomUser.objects.get(id = request.user.id)
        getuser.first_name = request.POST['new_first_name']
        getuser.last_name = request.POST['new_last_name']
        getuser.phone = request.POST['new_phone']
        getuser.save()
        if 'new_logo' in request.POST:
            getprofile = Profile.objects.get(owner = request.user)
            image = request.FILES['new_logo']
            fs = FileSystemStorage("media/logo/")
            filename = fs.save(image.name, image)
            image_url = settings.MEDIA_URL+"logo/"+filename
            getprofile.image = image_url
            getprofile.save()
        return HttpResponse("Success")

def login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        user = auth.authenticate(phone=phone, password=password)

        if user is not None:
            logo = Profile.objects.filter(owner = request.user.id)
            auth.login(request, user)
            return redirect('/', {'logo': logo})
        else:
            messages.info(request, 'Invalid username or password!')
            return redirect('login')

    else:
        return render(request, 'account/login.html')

def profile(request):
    Video = video.objects.all()
    likes = 0
    views = 0
    for Video in Video:
        if Video.likes.filter(id = request.user.id).exists():
            likes += 1
        if Video.views.filter(id = request.user.id).exists():
            views += 1
            
    current_user = request.user.id
    Channel = channel.objects.filter(owner = current_user)
    Channel_no = channel.objects.filter(owner = current_user).count()
    logo = Profile.objects.filter(owner_id = current_user)
    context = {
        "channel":Channel,
        "no_channel":Channel_no,
        'logo': logo,
        'likes': likes,
        'views': views,
    }
    return render(request, 'profile/profile.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')