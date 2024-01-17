from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker

from customers.models import CustomUser
from orders.models import Order, OrderItem, Receipt
from product.models import Products

user = get_user_model()


class OrderModelTest(TestCase):
    def setUp(self):
        self.customuser = baker.make(user, firstname='sahar', lastname='mahmoodi')
        self.order = baker.make(Order, user=self.customuser, status='order')

    def test_order_str_method(self):
        """Test __str__ method"""
        expected_str = self.customuser
        self.assertEqual(str(self.order), str(expected_str))


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = baker.make(CustomUser, firstname='sahar', lastname='mahmoudishad')
        self.product = baker.make(Products, detail='0')
        self.order = Order.objects.create(user=self.user, status='order')
        self.orderitem = OrderItem.objects.create(quantity=2, delivery_cost=5, order=self.order)
        self.orderitem.items.add(self.product)

    def test_order_item_creation(self):
        """Test if the OrderItem was created successfully """
        self.assertEqual(self.orderitem.quantity, 2)
        self.assertEqual(self.orderitem.delivery_cost, 5)
        self.assertEqual(self.orderitem.order, self.order)
        self.assertEqual(self.orderitem.items.count(), 1)

    def test_order_item_str_method(self):
        """Test the __str__ method"""
        self.assertEqual(str(self.orderitem), str(self.order))


class ReceiptModelTest(TestCase):

    def setUp(self):
        self.user = baker.make(CustomUser, firstname='sahar', lastname='mahmoudishad')
        self.order = Order.objects.create(user=self.user, status='order')
        self.receipt = Receipt.objects.create(order=self.order)

    def test_receipt_creation(self):
        """Check if the Receipt was created successfully"""
        self.assertIsInstance(self.receipt, Receipt)
        self.assertEqual(self.receipt.order, self.order)
        self.assertIsNotNone(self.receipt.time)

    def test_receipt_str_method(self):
        """Create a Receipt instance"""
        expected_str = f"{self.receipt.time}"
        self.assertEqual(str(self.receipt), expected_str)

    def test_receipt_order_relation(self):
        """Retrieve the related Order"""
        related_order = self.receipt.order

        """Check if the related Order is the same as the one we associated with the Receipt"""
        self.assertEqual(related_order, self.order)

