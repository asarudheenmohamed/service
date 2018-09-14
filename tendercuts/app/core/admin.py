# Register your models here.
from django.contrib import admin

from app.core.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in UserProfile._meta.fields]


admin.site.register(UserProfile, UserProfileAdmin)
