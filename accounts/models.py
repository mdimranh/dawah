from channel.models import channel, video
from django.contrib.auth import models
from django.contrib.auth.models import User, auth
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models.deletion import CASCADE
from django.conf import settings
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    
    def create_user(self, phone, email, fullname, password):
        if not phone:
            raise ValueError('User must have a phone number.')

        phone = phone.title()
        email = email.title()
        fullname = fullname.title()

        user = self.model(
            phone = phone,
            email = email,
            fullname = fullname
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, email, fullname, password=None):
        user = self.create_user(
            phone,
            email = email,
            fullname = fullname,
            password = password
        )
        user.is_admin=True
        user.is_staff=True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    phone = models.CharField(max_length=20, verbose_name='User phone', default=None)
    email = models.EmailField(verbose_name='User email', unique=True)
    fullname = models.CharField(max_length=150, verbose_name='full name')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone', 'fullname')

    objects = CustomUserManager()

    def __str__(self):
       return self.fullname
    
    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        verbose_name_plural = 'Users'

    
class Profile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.TextField(default='/media/logo/default.jpg')
    following = models.ManyToManyField(channel, default=None, blank=True)
    notification_read_time = models.DateTimeField(default=now)

    def total_following(self):
        return self.following.count()

    def __str__(self):
        return str(self.owner)

    class Meta:
        verbose_name_plural = 'Users Profile'