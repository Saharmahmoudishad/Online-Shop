from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker
from orders.models import Order

user = get_user_model()


class OrderModelTest(TestCase):
    def setUp(self):
        self.customuser = baker.make(user, firstname='sahar', lastname='mahmoodi')
        self.order = baker.make(Order, user=self.customuser, status='order')

    def test_order_str_method(self):
        """Test __str__ method"""
        expected_str = self.customuser
        self.assertEqual(str(self.order), str(expected_str))


