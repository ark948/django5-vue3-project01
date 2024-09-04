from django.urls import path
from accounts.views import (
    AccountsIndexView,
    RegisterUserView,
    VerifyUserEmail
)

app_name = 'accounts'
urlpatterns = [
    path('', AccountsIndexView.as_view(), name='index'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify_email')
]