from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChaneForm
from .models import Profile

user = get_user_model()

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChaneForm

    list_display = ('phone', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_staff')
    list_filter = ('is_admin','is_active')

    fieldsets = (
        (
            None, {'fields':('phone', 'first_name', 'last_name', 'password')}
        ),
        (
            'permissions', {'fields': ('is_active', 'is_admin', 'is_staff')}
        )
    )

    add_fieldsets = (
        (
            None, {
                'fields':('phone', 'first_name', 'last_name', 'password', 'is_active', 'password1', 'password2')
            }
        ),
        ('permissions', {'fields':('is_admin', 'is_staff')})
    )

    ordering = ()
    search_fields = ('phone',)
    filter_horizontal = ()

admin.site.register(user, UserAdmin)
admin.site.register(Profile)