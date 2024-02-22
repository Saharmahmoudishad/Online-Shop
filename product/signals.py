from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import OrderItem
from product.models import Variants, Products


@receiver(post_save, sender=Variants)
def update_variant_status(sender, instance, **kwargs):
    if instance.quantity == 0:
        instance.status = False
        instance.save()

@receiver(post_save, sender=Products)
def update_variant_status(sender, instance, **kwargs):
    if instance.quantity == 0:
        instance.status = False
