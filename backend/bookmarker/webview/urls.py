from django.urls import path
from bookmarker.webview.views import (
    BookmarkerIndexView
)

app_name='web'
urlpatterns = [
    path('', BookmarkerIndexView.as_view(), name='index'),
]