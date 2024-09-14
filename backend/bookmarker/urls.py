from django.urls import path, include
from bookmarker.views import (
    BookmarkerRootAPIView
)

app_name = 'bookmarker'
urlpatterns = [
    path('webview/', include('bookmarker.webview.urls')),
    path('api/', include('bookmarker.api.urls')),
    path('', BookmarkerRootAPIView.as_view(), name='index'),
]