from rest_framework import serializers

from orders.models import OrderItem, Order


class OrderItemSerializer(serializers.ModelSerializer):
    items =serializers.StringRelatedField(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['quantity', 'items']


class OrderSerializer(serializers.ModelSerializer):
    orderitems = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'paid', 'order_time', 'delivery_cost', 'calculation',"orderitems", 'delivery_method', 'delivery_address']

    def get_orderitems(self, obj):
        customer_items = obj.orderItem.all()
        return OrderItemSerializer(instance=customer_items, many=True).data
