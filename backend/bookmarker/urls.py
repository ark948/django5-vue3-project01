from django.urls import path
from bookmarker.views import (
    UserBookmarksList,
    UserBookmarkDetails
)

app_name = 'bookmarker'
urlpatterns = [
    path('<int:pk>/', UserBookmarkDetails.as_view(), name='get_item'),
    path('', UserBookmarksList.as_view(), name='index'),
]