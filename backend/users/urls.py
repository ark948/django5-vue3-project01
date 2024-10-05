from django.urls import path, include
from users.views import *

app_name = 'users'
urlpatterns = [
    path('', index, name='index'),
]