from django.urls import path
from bookmarker.views import (
    UserBookmarksList,
    UserBookmarkDetailView,
)

app_name = 'bookmarker'
urlpatterns = [
    path('<int:pk>/', UserBookmarkDetailView.as_view(), name='get-item'),
    path('', UserBookmarksList.as_view(), name='index'),
]