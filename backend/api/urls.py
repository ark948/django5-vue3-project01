from django.urls import path, include
from api.views import (
    RootAPIView,
    TestFrontendConnection
)

urlpatterns = [
    path('', RootAPIView.as_view(), name='root'),
    path('test/', TestFrontendConnection.as_view(), name='test'),
    path('accounts/', include('accounts.urls')),
]