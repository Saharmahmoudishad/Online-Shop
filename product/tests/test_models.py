from unittest import TestCase

from django.urls import reverse
from model_bakery import baker

from core.models import Image
from product.models import Brand


class TestBrandModel(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(title='Test Brand', slug='test-brand')
        self.image = Image.objects.create(content_object=self.brand, image="/static/img/cat-1.jpg")

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.brand), 'Test Brand')

    def test_image_tag_with_images(self):
        """test image_tag method return brand logo from Image model """

        result = self.brand.image_tag()
        self.assertIsNotNone(result)
        self.assertIn('<img src="', result)
