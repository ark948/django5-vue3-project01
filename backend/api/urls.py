from django.urls import path, include
from api.views import (
    RootAPIView,
)

urlpatterns = [
    path('auth/', include('accounts.urls', namespace='accounts')),
    path('bookmarker/', include('bookmarker.urls')),
    path('', RootAPIView.as_view(), name='root'),
]