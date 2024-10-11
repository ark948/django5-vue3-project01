# django imports
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save 
from django.dispatch import receiver

# rest_framework imports
from rest_framework_simplejwt.tokens import RefreshToken

# local imports
from accounts.managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField('Username', unique=True, null=True, max_length=225)
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
    
    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = "User Profiles"

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    print("\n--> Profile signal called.\n")
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)

class OneTimePassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} - passcode'
