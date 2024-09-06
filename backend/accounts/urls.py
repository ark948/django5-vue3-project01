from django.urls import path
from accounts.views import (
    AccountsIndexView,
    RegisterUserView,
    VerifyUserEmail,
    LoginUserView,
    TestAuthenticationView
)

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify_email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('test-auth/', TestAuthenticationView.as_view(), name='test_auth'),
    path('', AccountsIndexView.as_view(), name='index'),
]