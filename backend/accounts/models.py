from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from accounts.managers import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.signals import post_save 
from django.dispatch import receiver


# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False) # my own
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
class UserProfile(models.Model):
    user = models.OneToOneField("accounts.CustomUser", on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"), null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"), null=True, blank=True)

    def __str__(self) -> str:
        return f'Profile for: {self.user}'

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = "User Profiles"

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    print("\n==> Creating user profile.")
    if created:
        UserProfile.objects.create(user=instance)
        print("\n==> User profile created successfully.\n")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print("\n==> User updated.\n")
        except:
            UserProfile.objects.create(user=instance)
            print('\n==> User profile created. ok.\n')

class OneTimePassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} - passcode'
