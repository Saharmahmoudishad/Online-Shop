from rest_framework import serializers

from orders.models import OrderItem, Order, Receipt


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity', 'delivery_cost', 'items']


class OrderSerializer(serializers.ModelSerializer):
    orderItem = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'paid', 'order_time', 'orderItem']


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['time', 'order', 'calculation']
