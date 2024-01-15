from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from product.models import Products

user = get_user_model()


class Order(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name="user_cart")
    status = models.CharField(max_length=10, default="order")
    order_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-order_time']
        indexes = [
            models.Index(fields=['-order_time'])
        ]

    @classmethod
    def get_absolute_url(cls):
        return reverse('order:cart-receipt', args=[user.id])

    def __str__(self):
        return f" {self.id}_{self.user}"


class OrderItem(models.Model):
    DoesNotExist = None
    quantity = models.PositiveIntegerField(default=1, blank=True)
    delivery_cost = models.PositiveIntegerField(null=True, blank=True, default=0)
    items = models.ManyToManyField(Products, related_name="item_order")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderItem")

    def __str__(self):
        return f"{self.order.id} "


class Receipt(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='receipt_order')


    class Meta:
        ordering = ['-time']
        indexes = [
            models.Index(fields=['-time'])
        ]

    def __str__(self):
        return f"{self.time}"
