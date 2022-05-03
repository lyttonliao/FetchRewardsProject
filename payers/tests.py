from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Payer


class PayerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_payer(self):
        payload = {'company': 'SampleCompany1'}
        res = self.client.post('/payers/', payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_payer_exists(self):
        payload = {'company': 'SampleCompany1'}
        Payer.objects.create(**payload)

        res = self.client.post('/payers/', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)