from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from accounts.serializers import *

class UserRegisterSerializerTest(APITestCase):
    def test_user_register_serializer_valid_data(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'home123*',
            'password2': 'home123*'
        }

        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_user_password_missmatch(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'home456*',
            'password2': 'home123*'
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'][0], "Passwords do not match.")

    def test_user_serializer_duplicate_email(self):
        CustomUser.objects.create_user(email='existinguser@example.com', first_name='test', last_name='user', password='home123*')
        data = {
            'email': 'existinguser@example.com',
            'first_name': 'test01',
            'last_name': 'user01',
            'password': 'home123*',
            'password2': 'home123*',
        }

        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())