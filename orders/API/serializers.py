from rest_framework import serializers

from orders.models import OrderItem, Order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity', 'items']


class OrderSerializer(serializers.ModelSerializer):
    orderItem = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'paid', 'order_time', 'orderItem', 'delivery_cost', 'calculation']
