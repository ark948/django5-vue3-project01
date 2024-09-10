from django.urls import path
from bookmarker.views import (
    UserBookmarksList
)

app_name = 'bookmarker'
urlpatterns = [
    path('', UserBookmarksList.as_view(), name='index'),
]