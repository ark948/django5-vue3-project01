from django.urls import path
from bookmarker.api.views import (
    UserBookmarksList,
    UserBookmarkDetailView,
    UserBookmarksListNoPagination
)

app_name='api'
urlpatterns = [
    path('<int:pk>/', UserBookmarkDetailView.as_view(), name='item'),
    path('no-paginate/', UserBookmarksListNoPagination.as_view(), name='list_no_pagination'),
    path('', UserBookmarksList.as_view(), name='list'),
]