from django.urls import path
from apps.users.views import RegistrationView


app_name = 'apps_users'
urlpatterns = [
    path('register', RegistrationView.as_view(), name='index'),
]