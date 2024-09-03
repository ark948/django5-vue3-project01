from api.views import RootAPIView
from django.urls import path, include

urlpatterns = [
    path('', RootAPIView.as_view(), name='root'),
    path('accounts/', include('accounts.urls')),
]