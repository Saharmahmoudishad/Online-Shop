from django.shortcuts import render, get_object_or_404
from django.views import View

from product.models import Products



class AllProductView(View):
    def get(self, request):
        products = Products.objects.all()
        return render(request, 'product/shop.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Products, slug=slug)
        return render(request, 'product/detail.html', {product: product})

    def post(self, request):
        pass
