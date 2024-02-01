from django.test import TestCase, RequestFactory
from django.urls import reverse
from model_bakery import baker
from product.models import Products, CategoryProduct
from product.views import AllProductView, ProductDetailView


class TestAllProductView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.categoryproduct = baker.make(CategoryProduct, title='Test category product')
        self.product = Products.objects.create(title="Sample Product", price=100.00, detail="", slug="0")
        self.product.category.add(self.categoryproduct)

    def test_sort_latest(self):
        request = self.factory.get(reverse('product:products'))
        response = AllProductView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_sort_expensive(self):
        request = self.factory.get(reverse('product:products'), {'sort': 'expensive'})
        response = AllProductView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    #
    def test_sort_cheapest(self):
        request = self.factory.get(reverse('product:products'), {'sort': 'cheapest'})
        response = AllProductView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.product.category.clear()
        self.product.delete()
        self.categoryproduct.delete()


class TestProductDetailView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.product = baker.make(Products, slug='Sample_Product', detail="")

    def test_context_data(self):
        request = self.factory.get(reverse('product:product_detail', kwargs={'slug': 'Sample_Product'}))
        response = ProductDetailView.as_view()(request, slug='Sample_Product')

        self.assertEqual(response.status_code, 200)

        context_data = response.context_data

        self.assertIn('product', context_data)
        self.assertIn('product_variants', context_data)
        self.assertIn('product_images', context_data)
        self.assertIn('comments', context_data)
        self.assertIn('form', context_data)
        self.assertIn('form_reply', context_data)
