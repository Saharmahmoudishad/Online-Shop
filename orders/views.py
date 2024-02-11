from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.cart import Cart
from orders.models import Order, OrderItem
from orders.API.serializers import OrderSerializer, OrderItemSerializer
from product.models import Products, Variants, Size, Brand, Color, Material, Attribute
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CartView(View):
    template_name = 'orders/cart.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {"cart": cart, "data": list(cart.__iter__()),
                                                    "cart_total_price": cart.get_total_price()}, )
