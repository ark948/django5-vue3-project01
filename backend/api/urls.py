from django.urls import path, include
from api.views import (
    RootAPIView,
)

urlpatterns = [
    # path('auth/', include('accounts.urls')),
    path('bookmarker/', include('bookmarker.urls')),
    path('users/', include('users.urls')),
    path('', RootAPIView.as_view(), name='root'),
]