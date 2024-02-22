from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from core.API.serializers import ImageSerializer
from core.models import Image
from orders.models import OrderItem, Order
from product.models import Products


class OrderItemSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(read_only=True)
    item_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['quantity', 'items', 'item_image']

    def get_item_image(self, obj):
        try:
            image = Image.objects.filter(content_type=ContentType.objects.get_for_model(Products), object_id=obj.items.product.id).first()
            return ImageSerializer(instance=image).data
        except Image.DoesNotExist:
            return None


class OrderSerializer(serializers.ModelSerializer):
    orderitems = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'paid', 'order_time', 'delivery_cost', 'calculation', "orderitems", 'delivery_method',
                  'delivery_address']

    def get_orderitems(self, obj):
        customer_items = obj.orderItem.all()
        return OrderItemSerializer(instance=customer_items, many=True).data
