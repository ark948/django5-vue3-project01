from django.contrib import admin
from bookmarker.models import Bookmark, Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('owner', 'category')