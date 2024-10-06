from django.urls import path, include
from users.views import (
    index,
    RootAPIView,
    RegistrationView,
    CustomLoginView
)

app_name = 'users'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path(r'login/', CustomLoginView.as_view(), name='knox_login'),
    path(r'knox/auth/', include('knox.urls')),
    path('', index, name='index'),
]