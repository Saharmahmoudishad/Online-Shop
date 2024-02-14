from django.shortcuts import render
from django.views import View

from orders.cart import Cart


class CartView(View):
    template_name = 'orders/cart.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {"cart": cart, "data": list(cart.__iter__()),
                                                    "cart_total_price": cart.get_total_price()}, )


class CheckOutView(View):
    template_name = 'orders/checkout.html'

    def get(self, request):

        # cart = Cart(request)
        return render(request, self.template_name, )
