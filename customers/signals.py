from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from customers.models import CustomUser


@receiver(post_save, sender=CustomUser)
def add_to_customers_group(sender, instance, created, **kwargs):
    if created:
        customers_group, _ = Group.objects.get_or_create(name='customers')
        instance.groups.add(customers_group)