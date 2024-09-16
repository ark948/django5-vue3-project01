from django.urls import path
from rest_framework.routers import DefaultRouter
from bookmarker.api.views import (
    UserBookmarksList,
    UserBookmarkDetailView,
    UserBookmarksListNoPagination,
    BookmarkViewSet
)

app_name='api'
router = DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')
urlpatterns = [
    path('<int:pk>/', UserBookmarkDetailView.as_view(), name='item'),
    path('no-paginate/', UserBookmarksListNoPagination.as_view(), name='list_no_pagination'),
    path('', UserBookmarksList.as_view(), name='list'),
]

urlpatterns += router.urls