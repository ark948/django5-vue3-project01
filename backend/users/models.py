from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class CustomUser(AbstractUser):
    pass

    def __str__(self) -> str:
        return f'{self.email}'
    

class UserProfile(models.Model):
    user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE,)

    def __str__(self) -> str:
        return f'{self.user.email}'
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    
@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    print("\n==> Creating user profile.")
    if created:
        UserProfile.objects.create(user=instance)
        print("\n==> User profile created successfully.")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print("\n==> User updated.")
        except:
            UserProfile.objects.create(user=instance)
            print('\n==> User profile created. ok.')