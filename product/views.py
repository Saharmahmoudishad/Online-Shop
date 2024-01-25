from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from core.models import Image, Comment
from product.forms import CommentToManagerForm
from product.models import Products, Variants


class AllProductView(ListView):
    """ show all of the products
    sorting products is handled in this view
    """
    model = Products
    template_name = 'product/shop.html'
    context_object_name = 'products'
    paginate_by = 10

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
            min_price, max_price = map(int, price_range.split('-'))
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset


class ProductDetailView(DetailView):
    """ show detail of the product base on variants data of product
    login user can send comment in this part
    """
    model = Products
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(self.model, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_variants = Variants.objects.filter(product=context['product'])
        product_images = Image.objects.filter(content_type=ContentType.objects.get_for_model(Products),
                                              object_id=context['product'].id)
        product_content_type = ContentType.objects.get_for_model(Products)
        comments = Comment.objects.filter(content_type=product_content_type, object_id=context['product'].id)
        form = CommentToManagerForm
        context['comments'] = comments
        context['product_images'] = product_images
        context['product_variants'] = product_variants
        context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CommentToManagerForm(request.POST)
            if form.is_valid():
                datas = form.cleaned_data
                product_id = self.get_object().id
                new_comment = Comment.objects.create(
                    content=datas["content"],
                    content_type=ContentType.objects.get_for_model(Products),
                    object_id=product_id,
                    user=request.user,
                )
                messages.success(request, 'Comment added successfully.')
        return self.get(request, *args, **kwargs)
