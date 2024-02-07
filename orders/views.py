from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.cart import Cart
from orders.forms import CartAddForm
from orders.models import Order, OrderItem
from product.models import Products, Variants, Size, Brand, Color, Material, Attribute


class CartView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/cart.html'

    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"cart": cart, "data": list(cart.__iter__()),
             "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
        )

    def post(self, request, product_id, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Products, id=product_id)


        if "remove" in request.data:
            variant = request.data["variant"]
            cart.remove(variant)

        elif "clear" in request.data:
            cart.clear()

        else:
            variant = request.data

            post_data = {key: int(value[0:20]) if value.isdigit() else value[0:20] for key, value in
                         request.data.items()}
            print("!"*50,post_data)
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

            cart.add(variant=variant_chose,
                     discount_price=post_data['discount'],
                     quantity=post_data['quantity'],
                     brand=post_data['brand'].title,
                     color=post_data['color'].name,
                     size=post_data['size'].code,
                     material=post_data['material'].name,
                     attribute=post_data['attribute'].type, )
            product = get_object_or_404(Products, id=product_id)

        return Response(
            {"message": "cart updated", 'cart': cart, 'product': product},
            status=status.HTTP_202_ACCEPTED)

