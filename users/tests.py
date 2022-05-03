from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


class UserAPITests(TestCase):
    """Test the Users API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test creating user with valid payload"""
        payload = {
            'email': 'test1@gmail.com',
            'password': 'test123890',
            'username': 'test1'
        }
        res = self.client.post('/users/', payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists"""
        payload = {
            'email': 'test1@gmail.com',
            'password': 'test123890',
            'username': 'test1'
        }
        get_user_model().objects.create_user(**payload)

        res = self.client.post('/users/', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        payload = {'email': 'test1@gmail.com', 'password': 'sho', 'username': 'test1'}
        res = self.client.post('/users/', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
