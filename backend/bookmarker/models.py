from django.db import models
from django.conf import settings

# Create your models here.
# each bookmark can have one category
# each category can have many bookmarks

class Category(models.Model):
    title = models.CharField("Title", max_length=60)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f'Bookmarks Category: {self.title}'

class Bookmark(models.Model):
    title = models.CharField("Title", max_length=120)
    url = models.URLField("URL")
    icon = models.ImageField("Icon", blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookmarks')

    def __str__(self):
        return f'bookmark entry for {self.owner}'
    