from django.urls import path
from accounts.views import AccountsIndexView

app_name = 'accounts'
urlpatterns = [
    path('', AccountsIndexView.as_view(), name='index'),
]