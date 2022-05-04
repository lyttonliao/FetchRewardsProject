from django.db import IntegrityError
from django.test import TestCase

from core import models


class ModelsTestCase(TestCase):
    def setUp(self):
        """Creates sample user, payer, and transaction"""
        self.user = models.User.objects.create(username='testing1')

        self.payer = models.Payer.objects.create(company='SampleCompany')

        self.transaction = models.Transaction.objects.create(
            user=self.user,
            payer=self.payer,
            points=500
        )

    def test_user_is_valid(self):
        """Tests if sample user was created with correct credentials and value"""
        self.assertEqual(self.user.username, 'testing1')
        self.assertEqual(self.user.points, 0)

    def test_user_without_username(self):
        """Tests if sample user can be created without a username"""
        with self.assertRaises(IntegrityError):
            models.User.objects.create(username=None)

    def test_payer_is_valid(self):
        """Test if payer's company name is equal to payer's string representation"""
        self.assertEqual(str(self.payer), self.payer.company)

    def test_transaction_is_valid(self):
        """Test if transaction object was created with correct references and values"""
        self.assertEqual(self.transaction.user, self.user)
        self.assertEqual(self.transaction.payer, self.payer)
        self.assertEqual(self.transaction.points, 500)