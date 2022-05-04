from django.test import TestCase

from core.models import User, Payer
from rest_framework import status
from rest_framework.test import APIClient


class UserAPITests(TestCase):
    """Test the Users API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test creating user with valid payload"""
        payload = {
            'username': 'testing1'
        }
        res = self.client.post('/users/', payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_exists(self):
        """Test creating a user that already exists"""
        payload = {
            'username': 'testing1'
        }
        User.objects.create(**payload)

        res = self.client.post('/users/', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
