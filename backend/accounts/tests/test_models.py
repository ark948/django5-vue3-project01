from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
import unittest

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
    def test_get_full_name(self):
        User = get_user_model()
        user = User.objects.create(email='test@example.com')
        
        self.assertEqual(user.get_full_name, "Test User")
        self.assertFalse(user.is_staff)