from django.contrib import admin
from accounts.models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_verified', 'date_joined')

admin.site.register(CustomUser, CustomUserAdmin)
