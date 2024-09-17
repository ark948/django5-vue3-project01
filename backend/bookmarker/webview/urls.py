from django.urls import path
from bookmarker.webview.views import (
    BookmarkerIndexView,
    BookmarksListView
)

app_name='web'
urlpatterns = [
    path('list', BookmarksListView.as_view(), name='list'),
    path('', BookmarkerIndexView.as_view(), name='index'),
]