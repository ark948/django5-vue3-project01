from rest_framework.test import APITestCase
from bookmarker.models import Bookmark
from django.contrib.auth import get_user_model

class BookmarkerSerializersTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            first_name="test",  
            last_name="user",
            email="testuser@test.com", 
            password="testpass123"
        )
        cls.bookmark = Bookmark.objects.create(
            title="some title", url="www.someurl.com",
            owner=cls.user
        )