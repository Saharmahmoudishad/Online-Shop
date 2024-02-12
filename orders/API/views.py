import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import DiscountCode
from customers.models import Address
from customers.serializers import AddressSerializer, CustomUserSerializer
from orders.cart import Cart
from orders.models import Order, OrderItem
from orders.API.serializers import OrderSerializer, OrderItemSerializer
from product.models import Products, Variants, Size, Brand, Color, Material, Attribute
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CartAddProductView(APIView):
    def get(self, request):
        cart = Cart(request)
        return Response(
            {"cart": cart},
            status=status.HTTP_200_OK)

    def post(self, request, product_id=None, **kwargs):
        cart = Cart(request)
        post_data = {key: int(value[0:20]) if value.isdigit() else value[0:20] for key, value in
                     request.data.items()}
        post_data['size'] = Size.objects.filter(code=post_data['size']).first()
        post_data['brand'] = Brand.objects.filter(title=post_data['brand']).first()
        post_data['color'] = Color.objects.filter(name=post_data['color']).first()
        post_data['material'] = Material.objects.filter(name=post_data['material']).first()
        post_data['attribute'] = Attribute.objects.filter(type=post_data['attribute']).first()
        variant_chose = get_object_or_404(Variants, product=product_id,
                                          brand=post_data['brand'],
                                          size=post_data['size'], color=post_data['color'],
                                          material=post_data['material'],
                                          attribute=post_data['attribute'], )
        if post_data['quantity'] > variant_chose.quantity or variant_chose.quantity == 0:
            return Response({
                "message": f"The requested quantity is more than the stock of the product. the stock ={variant_chose.quantity}"},
                status=status.HTTP_400_BAD_REQUEST)
        cart.add(variant=variant_chose,
                 discount_price=post_data['discount'],
                 quantity=post_data['quantity'],
                 brand=post_data['brand'].title,
                 color=post_data['color'].name,
                 size=post_data['size'].code,
                 material=post_data['material'].name,
                 attribute=post_data['attribute'].type, )

        return Response(status=status.HTTP_200_OK)

    def put(self, request, variant_id=None):
        cart = Cart(request)
        variant_chose = get_object_or_404(Variants, id=variant_id)
        try:
            data = json.loads(request.body)
            new_quantity = int(data['quantity'])
            if new_quantity > variant_chose.quantity or variant_chose.quantity == 0:
                return Response({
                    "message": f"The requested quantity is more than the stock of the product."}, )
            cart.update(variant_id, new_quantity)
            return Response(
                {"message": "Cart updated successfully"},
                status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response(
                {"message": "Invalid JSON data"},
                status=status.HTTP_400_BAD_REQUEST)


class CartRemoveView(APIView):

    def get(self, request, variant_id):
        cart = Cart(request)
        variant = get_object_or_404(Variants, id=variant_id)
        cart.remove(variant)
        return Response('orders:cart')


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReciptView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, calculation=cart.get_total_price())

        for item in cart:
            product = get_object_or_404(Products, id=item['variant']['product'])
            OrderItem.objects.create(order=order, items=product, quantity=item['quantity'])
        cart.clear()

        ser_data = OrderSerializer(order)
        print("1" * 50, ser_data.data)
        return JsonResponse(ser_data.data, status=status.HTTP_201_CREATED)

    def post(self, request):
        discountcode = request.data['discountcode']
        discount_factor = DiscountCode.objects.get(title=discountcode)
        order = Order.objects.get(id=149)
        order.calculation = float(order.calculation) * float(discount_factor.amount)
        order.save()

        return Response(status=status.HTTP_200_OK)

    def put(self, request, order_id):
        oderitem = OrderItem.objects.create(order=order_id)
        ser_data = OrderItemSerializer(instance=oderitem, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        order = Order.objects.create(id=order_id)
        order.logical_delete()
        return Response('message:orders deleted by user')


class CheckOutView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        print("12" * 50, request.user)
        if request.user.is_authenticated:
            user = request.user
            try:
                address = Address.objects.get(user=user)
                print("13" * 50, address)
            except Address.DoesNotExist:
                raise NotFound("User address not found")
            address_serializer = AddressSerializer(instance=address)
            user_serializer = CustomUserSerializer(instance=user)
            print("14" * 50, {
                "user": user_serializer.data,
                "address": address_serializer.data
            })
            return Response({
                "user": user_serializer.data,
                "address": address_serializer.data
            })
        else:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
