from django.contrib import admin
from .models import UserModel, UserConfig
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry

LogEntry._meta.get_field('user').remote_field.model = UserModel

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_staff', 'is_superuser')
    list_filter = ('is_admin', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(UserModel, CustomUserAdmin)
admin.site.register(UserConfig)