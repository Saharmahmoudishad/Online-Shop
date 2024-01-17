from unittest import TestCase
from model_bakery import baker
from core.models import Image
from product.models import Brand, Size, Material, Color, Attribute, CategoryProduct, Products, Variants


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
        self.brand.hard_delete()
        self.image.hard_delete()
        self.brand2.hard_delete()


class TestSizeModel(TestCase):
    def setUp(self):
        self.size = Size.objects.create(gender='test_size', code='test-Size')

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.size), 'test_size')

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.size.hard_delete()


class TestMaterialModel(TestCase):
    def setUp(self):
        self.material = Material.objects.create(name='test_material')

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.material), 'test_material')

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.material.hard_delete()


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
        self.color_with_code.hard_delete()
        self.color_without_code.hard_delete()


class TestAttributeModel(TestCase):
    def setUp(self):
        self.attribute = Attribute.objects.create(attribute='test_attribute', type='test_type')

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.attribute), 'test_attribute_test_type')

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.attribute.hard_delete()


class CategoryProductModelTest(TestCase):
    def setUp(self):
        self.categoryproduct = baker.make(CategoryProduct, title='Test category product', )
        self.child_category = baker.make(CategoryProduct, title="Child Category", parent=self.categoryproduct,
                                         tags="child, category", description="Child category description")

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.categoryproduct), 'Test category product')

    def test_category_has_children(self):
        self.assertIn(self.child_category, self.categoryproduct.children.all())

    def test_category_has_no_parent(self):
        self.assertIsNone(self.categoryproduct.parent)

    def test_category_has_keywords(self):
        # Test if a category has keywords
        self.assertEqual(self.child_category.tags, "child, category")

    def test_category_has_description(self):
        # Test if a category has a description
        self.assertEqual(self.child_category.description, "Child category description")

    def tearDown(self):
        """Delete the test data created in setUp"""
        self.categoryproduct.hard_delete()
        self.child_category.hard_delete()


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
        self.product.hard_delete()
        self.image.hard_delete()


class TestVariantsModel(TestCase):
    def setUp(self):
        self.product = baker.make(Products, title='Test product', detail="")
        self.variant = baker.make(Variants, title='Test variant', product=self.product)
        self.image = Image.objects.create(content_object=self.variant, image="/static/img/cat-1.jpg")

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
        self.product.hard_delete()
        self.variant.hard_delete()
        self.image.hard_delete()
