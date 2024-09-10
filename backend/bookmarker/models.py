from django.db import models
from django.conf import settings

# Create your models here.

class Bookmark(models.Model):
    title = models.CharField("Title", max_length=32)
    url = models.URLField("URL")
    icon = models.ImageField("Icon")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')

    def __str__(self):
        return f'bookmark entry for {self.owner}'
    