from django.contrib import admin
from .models import UserProfile


# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "phone_number")
    search_fields = ("user__username", "user__email", "address", "phone_number")