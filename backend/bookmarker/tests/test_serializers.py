from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bookmarker.models import Bookmark
from accounts.managers import UserManager
from bookmarker.serializers import BookmarksSerializer
from accounts.models import CustomUser


class BookmarkerSerializersTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        CustomUser.objects.create_user(
            email='existinguser@example.com',
            first_name='test',
            last_name='user',
            password='home123*'
        )
        return super().setUpTestData()

    def test_serializer_data_is_valid(self):

        data = {
            'title': 'some title',
            'url': 'https://someurl.com/',
            'icon': None,
            'owner': CustomUser.objects.get(id=1),
        }

        serializer = BookmarksSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_data_is_not_valid(self):
        data = {
            'title': 'some title',
            'url': 'incorrect url address',
            'icon': None,
            'owner': CustomUser.objects.get(id=1),
        }
        serializer = BookmarksSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['url'][0], "Enter a valid URL.")
