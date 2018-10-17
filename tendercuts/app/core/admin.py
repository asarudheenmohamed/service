# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from app.core.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in UserProfile._meta.fields]


admin.site.register(UserProfile, UserProfileAdmin)

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileInlineAdmin(UserAdmin):
    inlines = [UserProfileInline, ]

admin.site.register(User, UserProfileInlineAdmin)
