from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from core.models import Image, Comment
from product.forms import CommentToManagerForm, CommentReplyForm
from product.models import Products, Variants, CategoryProduct


class AllProductView(ListView):
    """ show all of the products
    sorting products is handled in this view
    """
    model = Products
    template_name = 'product/shop.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Products.objects.filter(is_deleted=False)
        slug = self.kwargs.get('slug', None)
        category = get_object_or_404(CategoryProduct, slug=slug) if slug else None
        queryset = queryset.filter(category=category.id) if category else queryset
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

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {"products": products})


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
        comments = Comment.objects.filter(content_type=product_content_type, object_id=context['product'].id,
                                          parent_comment__isnull=True)
        form = CommentToManagerForm
        form_reply = CommentReplyForm
        context['comments'] = comments
        context['product_images'] = product_images
        context['product_variants'] = product_variants
        context['form'] = form
        context['form_reply'] = form_reply

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


class LoginRequireMixin:
    pass


class ReplyProductCommentView(LoginRequireMixin, View):
    form_class = CommentReplyForm

    def post(self, request, product_slug, comment_id):
        product = get_object_or_404(Products, slug=product_slug)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            datas = form.cleaned_data
            reply = form.save(commit=False)
            reply.content = datas["content"]
            reply.content_type = ContentType.objects.get_for_model(Products)
            reply.object_id = product.id
            reply.user = request.user
            reply.parent_comment = comment
            # reply.is_reply = True
            reply.save()
        return redirect ('product:product_detail', product.slug)



