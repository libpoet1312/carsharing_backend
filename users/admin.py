from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password', 'avatar')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff')
        })
    )

    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password', 'avatar', 'country', 'phone_number', 'dob', 'gender')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff')
        })
    )

    list_display = ['username', 'email', 'date_joined',]
    search_fields = ('email', 'username')
    ordering = ('date_joined',)


admin.site.register(User, UserAdmin)

