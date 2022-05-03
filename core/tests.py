from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelsTestCase(TestCase):
    def setUp(self):
        """Creates sample user, payer, and transaction"""
        self.user = get_user_model().objects.create_user(
            username='test1', email='test1@gmail.com', password='test123890')

        self.payer = models.Payer.objects.create(company='SampleCompany')

        self.transaction = models.Transaction.objects.create(
            user=self.user,
            payer=self.payer,
            points=500
        )


    def test_user_is_valid(self):
        """Tests if sample user was created with correct credentials and value"""
        self.assertEqual(self.user.email, 'test1@gmail.com')
        self.assertEqual(self.user.points, 0)
        self.assertTrue(self.user.check_password('test123890'))

    
    def test_user_without_username(self):
        """Tests if sample user can be created without a username"""
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                username=None, email='test2@gmail.com', password='test123890')

    
    def test_user_without_email(self):
        """Tests if sample user can be created without an email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username='test2', email=None, password='test123890')


    def test_payer_is_valid(self):
        """Test if payer's company name is equal to payer's string representation"""
        self.assertEqual(str(self.payer), self.payer.company)


    def test_transaction_is_valid(self):
        """Test if transaction object was created with correct references and values"""
        self.assertEqual(self.transaction.user, self.user)
        self.assertEqual(self.transaction.payer, self.payer)
        self.assertEqual(self.transaction.points, 500)