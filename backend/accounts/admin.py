from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser, OneTimePassword, UserProfile
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Profile"

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "username")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        (None, {"fields": ('is_verified',)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    inlines = [UserProfileInline]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OneTimePassword)
admin.site.register(UserProfile) 