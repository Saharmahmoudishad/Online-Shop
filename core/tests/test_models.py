from unittest import TestCase

from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from model_bakery import baker

from core.models import Comment, Image, Province, City, DiscountCode
from customers.models import CustomUser


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = baker.make(CustomUser, firstname='sahar', lastname='mahmoudishad')
        self.content_type, created = ContentType.objects.get_or_create(model='testmodel', app_label='testapp')

        self.comment = Comment.objects.create(content='Test content', content_type=self.content_type, object_id=1,
                                              user=self.user)

        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.image = Image.objects.create(image=image_file, content_type=self.content_type, object_id=1)
        # Image.objects.create(image='path/to/employee_image.jpg',
        #                      content_type=ContentType.objects.get_for_model(Employee), object_id=employee.id)

        self.province = Province.objects.create(name='Test Province')

        self.city = City.objects.create(name='Test City', province=self.province)

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'Test content')
        self.assertEqual(self.comment.user, self.user)

    def test_image_creation(self):
        self.assertIsNotNone(self.image.image)
        self.assertEqual(self.image.content_type, self.content_type)

    def test_province_creation(self):
        self.assertEqual(self.province.name, 'Test Province')

    def test_city_creation(self):
        self.assertEqual(self.city.name, 'Test City')
        self.assertEqual(self.city.province, self.province)


class DiscountCodeTest(TestCase):

    def setUp(self):
        self.content_type, created = ContentType.objects.get_or_create(model='testmodel', app_label='testapp')
        self.discount_code = DiscountCode.objects.create(title='Test Discount', amount=10.00,
                                                         deadline=timezone.now() + timezone.timedelta(days=7), content_type=self.content_type,
                                                         object_id=1)

    def test_discount_code_creation(self):
        self.assertEqual(self.discount_code.title, 'Test Discount')
        self.assertEqual(self.discount_code.amount, 10.00)
        self.assertTrue(self.discount_code.deadline > timezone.now())
        self.assertEqual(self.discount_code.content_type, self.content_type)
        self.assertEqual(self.discount_code.object_id, 1)

    def test_discountcode_str_method(self):
        self.assertEqual(str(self.discount_code), 'Test Discount_10.0')