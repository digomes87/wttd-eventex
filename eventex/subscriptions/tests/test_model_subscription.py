from django.test import TestCase
from eventex.subscriptions.models import Subscription
from datetime import datetime

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Diego Gomes',
            cpf='0151679412',
            email='diego.gomes87@gmail.com',
            phone='4195062619'
        )
        self.obj.save()

    def test_create(self):  
        self.assertTrue(Subscription.objects.exists())

    def test_create_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)
    
    def test_str(self):
        self.assertEqual('Diego Gomes', str(self.obj))