from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bookmarker.models import Bookmark
from accounts.managers import UserManager

class BookmarkerSerializersTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserManager.create_user(email="testuser01@gmail.com", password="home123*")
        cls.bookmark = Bookmark.objects.create(title="some title", url="www.someurl.com", owner=cls.user)