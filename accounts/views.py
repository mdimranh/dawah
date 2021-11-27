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

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render

from .models import EmailConfirmed

User = get_user_model()

@csrf_exempt
def signup(request):
    if request.method == 'POST' and request.FILES['image']:
        if 'fullname' in request.POST:
            email = request.POST['email']
            print(email)
            phone = request.POST['phone']
            fullname = request.POST['fullname']
            password = request.POST['password']

            if User.objects.filter(email=email).exists():
                messages.info(request,'This email is already exist.')
                return redirect('signup')
            else:
                user = User.objects.create_user(email=email, phone=phone, password=password, fullname=fullname)
                user.is_active = False
                user.save()
                euser = EmailConfirmed.objects.get(user = user)
                site = get_current_site(request)
                email = user.email
                email_body = render_to_string(
                    'account/verify.html',
                    {
                        'email': email,
                        'domain': site.domain,
                        'activation_key': euser.activation_key
                    }
                )
                send_mail(
                    subject='Email Confirmation',
                    message=email_body,
                    from_email='mdimranh.cse@gmail.com',
                    recipient_list=[email],
                    fail_silently=True
                )
                messages.success(request, "Account created successfull. We will send you link in your email for active your account. Please active your account by click the link.")

                image = request.FILES['image']
                fs = FileSystemStorage("media/logo/")
                filename = fs.save(image.name, image)
                image_url = settings.MEDIA_URL+"logo/"+filename
                Owner = CustomUser.objects.get(email = email)
                profile = Profile(
                    owner = Owner,
                    image = image_url,
                )
                profile.save()
                return redirect('login')
        
        if 'new_fullname' in request.POST:
            getuser = CustomUser.objects.get(id = request.user.id)
            getuser.fullname = request.POST['new_fullname']
            getuser.email = request.POST['new_email']
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



def email_confirm(request, activation_key):
   euser = get_object_or_404(EmailConfirmed, activation_key = activation_key)
   if euser is not None:
       print(euser.user)
       euser.email_confirmd = True
       euser.save()
       
       user1 = User.objects.get(email = euser)
       user1.is_active = True
       user1.save()
       return render(request, 'account/success.html')

def password_recover(request, activation_key):
    if request.method == 'POST':
        if 'password' in request.POST:
            print(f"email = {request.POST['user_email']}")
            user = User.objects.get(email = request.POST['user_email'])
            user.set_password(request.POST['password'])
            user.save()
            messages.success(request, 'Password set successfully. Please login..')
            return redirect('/account/login')
    else:
        euser = get_object_or_404(EmailConfirmed, activation_key = activation_key)
        if euser is not None:
            euser.email_confirmd = True
            euser.save()
            return render(request, 'account/newpass.html', {'user_email': euser})

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
        if 'email' in request.POST:
            email = request.POST['email']
            password = request.POST['password']

            user = auth.authenticate(email=email, password=password)

            if user is not None:
                logo = Profile.objects.filter(owner = request.user.id)
                auth.login(request, user)
                return redirect('/', {'logo': logo})
            else:
                messages.info(request, 'Invalid username or password!')
                return redirect('login')
        elif 'recover-email' in request.POST:
            if User.objects.filter(email = request.POST['recover-email']).exists():
                user = User.objects.get(email = request.POST['recover-email'])
                #send email
                euser = EmailConfirmed.objects.get(user = user)
                site = get_current_site(request)
                email = user.email
                email_body = render_to_string(
                    'account/recover.html',
                    {
                        'email': email,
                        'domain': site.domain,
                        'activation_key': euser.activation_key
                    }
                )
                send_mail(
                    subject='Dawah Password recover',
                    message=email_body,
                    from_email='mdimranh.cse@gmail.com',
                    recipient_list=[email],
                    fail_silently=True
                )
                messages.success(request, "We will send you link in your email for recover your password. Please recover your password by click the link.")
                return redirect(request.path_info)
            else:
                messages.error(request, 'This email is not exists!!')
                return redirect(request.path_info)

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