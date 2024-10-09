from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
import unittest

# local imports
from accounts.models import UserProfile

# Create your tests here.

class CustomUserModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="testuser@test.com", 
            password="testpass123"
        )
        self.assertEqual(user.email, "testuser@test.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="admin@example.com", 
            password="testpass123"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class UserMethodTest(TestCase):
    @unittest.skip
    def test_get_full_name(self):
        User = get_user_model()
        user = User.objects.create(email='test@example.com')
        
        self.assertEqual(user.get_full_name, "Test User")
        self.assertFalse(user.is_staff)


class UserProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User = get_user_model()
        cls.user = User.objects.create_user('testuser01@gmail.com', password='home123*')
        cls.user.profile.first_name = 'test'
        cls.user.profile.last_name = 'user'
        return super().setUpTestData()

    def test_profile_was_created_successfully(self):
        self.assertIsInstance(self.user.profile, UserProfile)

    def test_profile_first_name(self):
        self.assertEqual(self.user.profile.first_name, 'test')

    def test_profile_last_name(self):
        self.assertEqual(self.user.profile.last_name, 'user')

    def test_profile_has_full_name(self):
        self.assertEqual(self.user.profile.get_full_name, 'test user')