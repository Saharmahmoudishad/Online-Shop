from unittest import TestCase

from django.utils import timezone
from model_bakery import baker
from core.models import Image
from product.models import Brand, Size, Material, Color, Attribute, CategoryProduct, Products, Variants, DiscountProduct


class TestBrandModel(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(title='test_brand', slug='test-brand')
        self.image = Image.objects.create(content_object=self.brand, image="/static/img/cat-1.jpg")
        self.brand2 = Brand.objects.create(title='test2_brand', )

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.brand), 'test_brand')

    def test_image_tag_with_images(self):
        """test image_tag method return brand logo from Image model """
        result = self.brand.image_tag()
        self.assertIsNotNone(result)
        self.assertIn('<img src="', result)

    def test_save_method_creates_slug(self):
        save_brand2 = Brand.objects.get(id=self.brand2.id)
        self.assertEquals(save_brand2.slug, 'test2_brand')

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.brand.delete()
        self.image.delete()
        self.brand2.delete()


class TestSizeModel(TestCase):
    def setUp(self):
        self.size = Size.objects.create(gender='test_size', code='test-Size')

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.size), 'test-Size')

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.size.delete()


class TestMaterialModel(TestCase):
    def setUp(self):
        self.material = Material.objects.create(name='test_material')

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.material), 'test_material')

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.material.delete()


class TestColorModel(TestCase):
    def setUp(self):
        self.color_with_code = Color.objects.create(name="test_color", code="#FF00F0")
        self.color_without_code = Color.objects.create(name="test_color_Without_Code")

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.color_with_code), 'test_color')

    def test_color_tag_with_code(self):
        """test color_tag method return  color with a code  """
        result = self.color_with_code.color_tag()
        expected_part = 'style="background-color:#FF00F0"'
        actual_result = result.replace(" ", "")
        self.assertIn(expected_part, actual_result)

    def test_color_tag_without_code(self):
        """Test the color_tag method for a color without a code"""
        result = self.color_without_code.color_tag()
        self.assertEqual(result, "")

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.color_with_code.delete()
        self.color_without_code.delete()


class TestAttributeModel(TestCase):
    def setUp(self):
        self.attribute = Attribute.objects.create(attribute='test_attribute', type='test_type')

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.attribute), 'test_attribute_test_type')

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.attribute.delete()


class CategoryProductModelTest(TestCase):
    def setUp(self):
        self.categoryproduct = CategoryProduct.objects.create(title='Test category product', )
        self.child_category = baker.make(CategoryProduct, title="Child Category", parent=self.categoryproduct,
                                         tags="child, category", description="Child category description")

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.categoryproduct), 'Test category product')

    def test_category_has_children(self):
        """Test TreeForeignKey """
        self.assertIn(self.child_category, self.categoryproduct.children.all())

    def test_category_has_no_parent(self):
        """Test TreeForeignKey """
        self.assertIsNone(self.categoryproduct.parent)

    def test_category_has_keywords(self):
        """Test if a category has keywords"""
        self.assertEqual(self.child_category.tags, "child, category")

    def test_category_has_description(self):
        """ Test if a category has a description"""
        self.assertEqual(self.child_category.description, "Child category description")

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.child_category.delete()
        self.categoryproduct.delete()


class TestProductModel(TestCase):
    def setUp(self):
        self.product = baker.make(Products, title='Test product', detail="")
        self.image = Image.objects.create(content_object=self.product, image="/static/img/cat-1.jpg")

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.product), 'Test product')

    def test_image_tag_with_images(self):
        """test image_tag method return image products from Image model """

        result = self.product.image_tag()
        self.assertIsNotNone(result)
        self.assertIn('<img src="', result)

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.product.delete()
        self.image.delete()


class TestVariantsModel(TestCase):
    def setUp(self):
        self.product = baker.make(Products, title='Test product', detail="")
        self.variant = baker.make(Variants, title='Test variant', product=self.product)
        self.image = Image.objects.create(content_object=self.variant, image="/static/img/cat-1.jpg")

    def test_default_values(self):
        """Test the default values of the model"""
        self.assertEqual(self.variant.price, 0)
        self.assertEqual(self.variant.quantity, 1)

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.variant), 'Test variant')

    def test_image_tag_with_images(self):
        """test image_tag method return image variant from Image model """

        result = self.variant.image_tag()
        self.assertIsNotNone(result)
        self.assertIn('<img src="', result)

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.product.delete()
        self.variant.delete()
        self.image.delete()


class DiscountProductTestCase(TestCase):
    def setUp(self):
        self.categoryproduct = baker.make(CategoryProduct, title='Test category product')
        self.product = Products.objects.create(title="Sample Product", price=100.00, category=self.categoryproduct, detail="", slug="0")
        self.discountproduct = baker.make(DiscountProduct,product=self.product)
        self.discountproduct2 = DiscountProduct.objects.create(title="Discounted Product", product=self.product,
                                                               deadline=timezone.now() + timezone.timedelta(days=7), amount=10.00, )

    def test_discountproduct_created(self):
        """Check the attributes of the DiscountProduct"""
        self.assertEqual(self.discountproduct2.title, "Discounted Product")
        self.assertEqual(self.discountproduct2.product, self.product)
        self.assertTrue(self.discountproduct2.deadline > timezone.now())
        self.assertEqual(self.discountproduct2.amount, 10.00)

    def test_model_str(self):
        """Check the __str__ representation of DiscountProduct"""
        self.assertEqual(str(self.discountproduct2), f"{self.discountproduct2.title}_{self.discountproduct2.amount}", )

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.product.delete()
        self.discountproduct.delete()
        self.discountproduct2.delete()
