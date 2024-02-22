from django.shortcuts import render, redirect
from django.views import View

from orders.cart import Cart
from orders.models import Order


class CartView(View):
    template_name = 'orders/cart.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {"cart": cart, "data": list(cart.__iter__()),
                                                    "cart_total_price": cart.get_total_price()}, )


class CheckOutView(View):
    template_name = 'orders/checkout.html'

    def get(self, request):
        return render(request, self.template_name, )


class CheckOutEndView(View):
    template_name = 'orders/checkout.html'

    def get(self, request):
        orderId = request.COOKIES.get('orderid')
        order = Order.objects.get(id=orderId)
        order.paid = True
        order.save()
        return redirect("core:home")
