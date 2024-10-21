from django.urls import path, include
from api.views import (
    RootAPIView,
    TestFrontendConnection
)

urlpatterns = [
    path('auth/', include('accounts.urls', namespace='accounts')),
    path('bookmarker/', include('bookmarker.urls')),
    path('test/', TestFrontendConnection.as_view(), name='test'),
    path('', RootAPIView.as_view(), name='root'),
]