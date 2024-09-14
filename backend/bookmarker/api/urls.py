from django.urls import path
from bookmarker.api.views import (
    UserBookmarksList,
    UserBookmarkDetailView
)

app_name='api'
urlpatterns = [
    path('<int:pk>/', UserBookmarkDetailView.as_view(), name='item'),
    path('', UserBookmarksList.as_view(), name='list'),
]