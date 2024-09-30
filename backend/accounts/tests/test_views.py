import unittest
from rest_framework.test import APITestCase
from django.urls import reverse

class UserRegisterViewTestCase(APITestCase):
    @unittest.skip
    def test_view_url_is_accessible_with_GET(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    @unittest.skip
    def test_view_url_is_accurate(self):
        response_with_reverse = self.client.get(reverse('accounts:register'))
        response_with_url = self.client.get('/api/register/')
        self.assertEquals(response_with_url.status_code, 200)
        self.assertEquals(response_with_reverse.status_code, response_with_url.status_code)

    @unittest.skip
    def test_view_post_with_valid_data(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'home123*',
            'password2': 'home123*'
        }

        response = self.client.post(reverse('accounts:register'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Hi, thanks for signing up. please check your email.')
        