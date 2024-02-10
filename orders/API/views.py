from django.http import JsonResponse
from django.shortcuts import get_object_or_404
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
    # renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/cart.html'

    def get(self, request):
        cart = Cart(request)

        return render(
            {"cart": cart, "data": list(cart.__iter__()),
             "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
        )


class CartAddProductView(APIView):
    template_name = 'product/shop.html'
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
        print("1"*50,cart)
        ser_data = OrderSerializer(order)
        return JsonResponse(ser_data.data, status=status.HTTP_201_CREATED)

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
