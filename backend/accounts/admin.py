from django.contrib import admin
from accounts.models import CustomUser, OneTimePassword


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OneTimePassword)