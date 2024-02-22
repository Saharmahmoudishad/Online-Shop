from datetime import timedelta
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView
from django.utils.translation import activate
from config.settings import CACHE_TTL
from product.models import CategoryProduct, Products


class IndexView(ListView):
    model = Products
    template_name = 'index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_level_categories = CategoryProduct.objects.filter(parent__isnull=True)
        category_data = []
        for category in top_level_categories:
            category_info = {
                'title': category.title,
                'image': category.image_tag(),
                'children': []}
            for child in category.get_descendants():
                child_info = {
                    'title': child.title,
                    'image': child.image_tag(), }
                category_info['children'].append(child_info)
            category_data.append(category_info)
        context['all_categories'] = category_data
        context['categories'] = CategoryProduct.objects.filter(parent__isnull=True)
        context['products'] = Products.objects.all()[:6]
        context['recent_products'] = Products.objects.filter(created__gte=timezone.now() - timedelta(days=6))[:4]
        return context


index_view_cached = cache_page(CACHE_TTL)(IndexView.as_view())


class ContactUsView(TemplateView):
    template_name = 'contact.html'


class ChangeLangView(View):
    def get(self, request, *args, **kwargs):
        language_code = request.GET.get('lang')
        next_url = request.GET.get('next', '/')

        if language_code:
            activate(language_code)

        return redirect(next_url)
