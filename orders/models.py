from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from translated_fields import TranslatedField
from django.utils.translation import gettext_lazy as _
from product.models import Products

user = get_user_model()


class Order(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name="user_cart")
    status = models.CharField(max_length=10, default="order", verbose_name=_("status"))
    order_time = models.DateTimeField(auto_now_add=True, verbose_name="order time")

    class Meta:
        ordering = ['-order_time']
        indexes = [models.Index(fields=['-order_time'])]
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    @classmethod
    def get_absolute_url(cls):
        return reverse('order:cart-receipt', args=[user.id])

    def __str__(self):
        return f"{self.user}"


class OrderItem(models.Model):
    DoesNotExist = None
    quantity = models.PositiveIntegerField(default=1, blank=True, verbose_name=_("quantity"))
    delivery_cost = TranslatedField(models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="delivery cost"))
    items = models.ManyToManyField(Products, related_name="item_order")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderItem")

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f"{self.order} "


class Receipt(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='receipt_order')

    class Meta:
        ordering = ['-time']
        indexes = [models.Index(fields=['-time'])]
        verbose_name = _('Receipt')
        verbose_name_plural = _('Receipts')

    def __str__(self):
        return f"{self.time}"
