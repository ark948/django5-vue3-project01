from django.urls import path
from accounts.views import (
    AccountsIndexView,
    RegisterUserView
)

app_name = 'accounts'
urlpatterns = [
    path('', AccountsIndexView.as_view(), name='index'),
    path('register/', RegisterUserView.as_view(), name='register'),
]