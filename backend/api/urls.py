from django.urls import path, include
from api.views import (
    RootAPIView,
    TestFrontendConnection,
    TestFrontendConnectionPost
)

urlpatterns = [
    path('test/', TestFrontendConnection.as_view(), name='test'),
    path('test-post/', TestFrontendConnectionPost.as_view(), name='test_post'),
    # path('auth/', include('accounts.urls')),
    path('bookmarker/', include('bookmarker.urls')),
    path('', RootAPIView.as_view(), name='root'),
]