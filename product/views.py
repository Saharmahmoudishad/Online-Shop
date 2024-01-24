from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView

from product.models import Products



# class AllProductView(View):
#     def get(self, request):
#         products = Products.objects.all()
#         return render(request, 'product/shop.html', {'products': products})
class AllProductView(ListView):
    model = Products
    template_name = 'product/shop.html'
    context_object_name = 'products'
    paginate_by = 10  # Set the number of products to display per page

    def get_queryset(self):
        sort_option = self.request.GET.get('sort', 'latest')

        if sort_option == 'latest':
            return Products.objects.all().order_by('-created')
        elif sort_option == 'expensive':
            return Products.objects.all().order_by('-price')
        elif sort_option == 'cheapest':
            return Products.objects.all().order_by('price')
        else:
            return Products.objects.all().order_by('-created')

class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Products, slug=slug)
        return render(request, 'product/detail.html', {product: product})

    def post(self, request):
        pass
