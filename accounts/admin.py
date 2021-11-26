from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChaneForm
from .models import Profile, EmailConfirmed

user = get_user_model()

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChaneForm

    list_display = ('email', 'phone', 'fullname', 'is_active', 'is_admin', 'is_staff')
    list_filter = ('is_admin','is_active')

    fieldsets = (
        (
            None, {'fields':('email', 'phone', 'fullname', 'password')}
        ),
        (
            'permissions', {'fields': ('is_active', 'is_admin', 'is_staff')}
        )
    )

    add_fieldsets = (
        (
            None, {
                'fields':('email', 'phone', 'fullname', 'password', 'is_active', 'password1', 'password2')
            }
        ),
        ('permissions', {'fields':('is_admin', 'is_staff')})
    )

    ordering = ()
    search_fields = ('email','phone',)
    filter_horizontal = ()

admin.site.register(user, UserAdmin)
admin.site.register(Profile)
admin.site.register(EmailConfirmed)