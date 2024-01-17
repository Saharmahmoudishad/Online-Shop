from unittest import TestCase

from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker

from core.models import Comment, Image, Province, City
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
