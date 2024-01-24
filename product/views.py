from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from product.models import Products, Variants


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
        queryset = Products.objects.all()
        # sorting logic
        sort_option = self.request.GET.get('sort', 'latest')
        if sort_option == 'latest':
            queryset = queryset.order_by('-created')
        elif sort_option == 'expensive':
            queryset = queryset.order_by('-price')
        elif sort_option == 'cheapest':
            queryset = queryset.order_by('price')

        price_range = self.request.GET.get('price', 'all')
        if price_range != 'all':
            # Extract min and max values from the price_range
            min_price, max_price = map(int, price_range.split('-'))
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset



class ProductDetailView(DetailView):
    model = Products
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'  # Use slug_url_kwarg instead of pk_url_kwarg

    def get_object(self, queryset=None):
        # Override get_object to use slug for lookup
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(self.model, slug=slug)

