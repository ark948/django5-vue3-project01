from django.urls import path
from bookmarker.views import (
    UserBookmarksList,
    UserBookmarkDetailView,
    BookmarkerIndexView,
    BookmarkerRootAPIView,
    BookmarkerHtmlRenderView
)

app_name = 'bookmarker'
urlpatterns = [
    path('webview/html', BookmarkerHtmlRenderView.as_view(), name='webview_html'),
    path('webview/index/', BookmarkerIndexView.as_view(), name='webview_index'),
    path('<int:pk>/', UserBookmarkDetailView.as_view(), name='get-item'),
    path('api/', UserBookmarksList.as_view(), name='get-list'),
    path('', BookmarkerRootAPIView.as_view(), name='index'),
]