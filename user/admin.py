from django.contrib import admin
from .models import User, UserConfig

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)
admin.site.register(UserConfig)