from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from orders.cart import Cart
from orders.forms import CartAddForm
from orders.models import Order, OrderItem
from product.models import Products


# Create your views here.
class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})




class CartAddView(PermissionRequiredMixin, View):

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Products, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
            return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Products, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order': order})


class OrderCreateView(LoginRequiredMixin, View):

    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, items=item['product'], quantity=item['quanlity'])
        cart.clear()
        return redirect('orders:oder_detail', order.id)
