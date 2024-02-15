from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from core.mixins import SoftDeleteMixin
from product.models import Products, Variants

user = get_user_model()


class Order(SoftDeleteMixin):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="user_cart", verbose_name=_("user"))
    paid = models.BooleanField(default=False, verbose_name=_("status"))
    order_time = models.DateTimeField(auto_now_add=True, verbose_name=_("order time"))
    delivery_cost = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name=_("delivery cost"))
    delivery_method = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name=_("delivery cost"))
    delivery_address = models.CharField(max_length=50,null=True, blank=True, default=0, verbose_name=_("delivery cost"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("updated"))
    calculation = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Calculation"))

    class Meta:
        ordering = ['paid', '-order_time']
        indexes = [models.Index(fields=['-order_time'])]
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    @classmethod
    def get_absolute_url(cls):
        return reverse('order:cart-receipt', args=[user.id])

    def __str__(self):
        return f"{self.user}"

    def get_total_price(self):
        return sum(item.get_cost for item in self.orderItem.all()) + self.delivery_cost


class OrderItem(SoftDeleteMixin):
    DoesNotExist = None
    quantity = models.PositiveIntegerField(default=1, blank=True, verbose_name=_("quantity"))
    items = models.ForeignKey(Variants, on_delete=models.CASCADE, related_name="orderItem", verbose_name=_("Items"))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderItem", verbose_name=_("order Item"))

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f"{self.order}"

    def get_cost(self):
        return self.items.price * self.quantity

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.quantity > self.items.quantity:
            messages.error('Code is expired', 'danger')
            raise ValidationError("The selected quantity is greater than available stock.")
        self.items.quantity -= self.quantity
        self.items.product.quantity -= self.quantity
        self.items.save()
