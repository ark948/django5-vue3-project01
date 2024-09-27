from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views.html_views import HTMLUserRegisterView
from accounts.views.json_views import (
    AccountsIndexView,
    RegisterUserView,
    VerifyUserEmail,
    LoginUserView,
    TestAuthenticationView,
    LogoutUserView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    SetNewPasswordView,
)

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify_email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('auth-required/', TestAuthenticationView.as_view(), name='auth_required'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),
    
    path('html-register/', HTMLUserRegisterView.as_view(), name='html_register'),
    path('', AccountsIndexView.as_view(), name='index'),
]