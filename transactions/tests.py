from django.test import TestCase

from core.models import User, Payer
from rest_framework import status
from rest_framework.test import APIClient


class UserPointsAPITests(TestCase):
    """Tests User API for adding and removing points"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testing1')
        self.payer_one = Payer.objects.create(company='Dannon')
        self.payer_two = Payer.objects.create(company='Unilever')
        self.payer_three = Payer.objects.create(company='Miller Coors')


    def test_user_receiving_points(self):
        """Tests if user is receiving points"""
        payload = {
            'user': self.user.id,
            'payer': self.payer_one.id,
            'points': 400
        }
        res = self.client.post('/transactions/', payload)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.points, 400)

        payload_two = {
            'user': self.user.id,
            'payer': self.payer_one.id,
            'points': 800
        }
        res = self.client.post('/transactions/', payload_two)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.points, 1200)

    
    def test_transactions_recorded_after_points_used(self):
        """Test if response correctly displays as multiple transactions"""
        payloads = [
            {
                "user": self.user.id,
                "payer": self.payer_one.id,
                "points": 1000,
                "timestamp": "2020-11-02T14:00:00Z"    
            },
            {
                "user": self.user.id,
                "payer": self.payer_two.id,
                "points": 200,
                "timestamp": "2020-10-31T11:00:00Z" 
            },
            {
                "user": self.user.id,
                "payer": self.payer_one.id,
                "points": -200,
                "timestamp": "2020-10-31T15:00:00Z"
            },
            {
                "user": self.user.id,
                "payer": self.payer_three.id,
                "points": 10000,
                "timestamp": "2020-11-01T14:00:00Z"
            },
            {
                "user": self.user.id,
                "payer": self.payer_one.id,
                "points": 300,
                "timestamp": "2020-10-31T10:00:00Z"
            }
        ]

        # Sorts transactions by time, necessary for points to be deducted 
        # from earliest positive transactions from the same payer
        payloads.sort(key=lambda x: x['timestamp'])
        for payload in payloads:
            self.client.post('/transactions/', payload)

        # Patch requests should add and subtract from user total, 
        # while deducting from earliest positive transactions
        update_res = self.client.patch('/users/' + str(self.user.id) + '/', {'points': 5000})
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.points, 6300)

        # Update_res is an array of dictionaries, iterate through 
        # the dictionaries to match the points deducted to the expected response
        expected_spend_call_res = {
            "Dannon": -100,
            "Unilever": -200,
            "Miller Coors": -4700,
        }
        for new_transaction in update_res.data:
            self.assertEqual(new_transaction['points'], expected_spend_call_res[new_transaction['payer']])

        # Point balance per payer when checking a player's points
        expected_point_balance_res = {
            "Dannon": 1000,
            "Unilever": 0,
            "Miller Coors": 5300,
        }
        point_balance_res = self.client.get('/users/' + str(self.user.id) + '/')
        self.assertEqual(point_balance_res.data, expected_point_balance_res)