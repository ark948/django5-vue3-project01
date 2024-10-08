from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.api.html_views import (
    HTMLIndexView,
    html_register_view,
    html_login_view,
    html_logout_view,
    html_verify_account,
    html_password_reset_request,
    html_password_reset_confirm,
    html_set_new_password,
    html_update_password,
    html_change_email,
    html_profile_page_view,
    html_edit_profile
)
from accounts.api.json_views import (
    AccountsIndexView,
    RegisterUserView,
    VerifyUserEmail,
    LoginUserView,
    TestAuthenticationView,
    LogoutUserView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    SetNewPasswordView,
    UpdatePasswordView,
    ChangeEmailView,
    GetProfile
)

app_name = 'accounts'
urlpatterns = [
    path('api/profile/<int:pk>/', GetProfile.as_view(), name='user_profile'),
    path('api/change-email/', ChangeEmailView.as_view(), name='change_email'),
    path('api/update-password/', UpdatePasswordView.as_view(), name='update_password'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/verify-email/', VerifyUserEmail.as_view(), name='verify_email'),
    path('api/login/', LoginUserView.as_view(), name='login'),
    path('api/logout/', LogoutUserView.as_view(), name='logout'),
    path('api/auth-required/', TestAuthenticationView.as_view(), name='auth_required'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),

    path('html-change-email', html_change_email, name='html_change_email'),
    path('html-update-password', html_update_password, name='html_update_password'),
    path('html-set-new-password', html_set_new_password, name='html_set_new_password'),
    path('html-password-reset-confirm/<uidb64>/<token>/', html_password_reset_confirm, name='html_password_reset_confirm'),
    path('html-edit-profile/', html_edit_profile, name='html_edit_profile'),
    path('html-profile/', html_profile_page_view, name='html_profile'),
    path('html-password-reset-request/', html_password_reset_request, name='html_password_reset_request'),
    path('html-verify/', html_verify_account, name='html_verify'),
    path('html-logout/', html_logout_view, name='html_logout'),
    path('html-login/', html_login_view, name='html_login'),
    path('html-register/', html_register_view, name='html_register'),
    path('html-index/', HTMLIndexView.as_view(), name='html_index'),

    path('', AccountsIndexView.as_view(), name='index'),
]