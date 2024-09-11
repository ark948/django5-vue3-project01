from bookmarker.models import Bookmark
from django.test import TestCase
from django.contrib.auth import get_user_model

class BookmarkModelTests(TestCase):
    @classmethod
    def testUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            first_name="test",  
            last_name="user",
            email="testuser@test.com", 
            password="testpass123"
        )
        cls.bookmark = Bookmark.objects.create(
            title="some title",
            url="http://www.sometitle.com/",
            owner=cls.user
        )

        
    def test_bookmark_model_attributes(self):
        self.assertEqual(self.bookmark.title, 'some title')
        self.assertEqual(self.bookmark.url, "http://www.sometitle.com/")

    def test_bookmark_model_relation(self):
        self.assertIsInstance(self.bookmark.owner, type(self.user))
        