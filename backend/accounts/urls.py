from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import (
    AccountsIndexView,
    RegisterUserView,
    VerifyUserEmail,
    LoginUserView,
    TestAuthenticationView,
    LogoutUserView
)

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify_email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('auth-required/', TestAuthenticationView.as_view(), name='auth_required'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('', AccountsIndexView.as_view(), name='index'),
]