from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField

from core.models import Image
from customers.models import CustomUser


class Brand(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)

    def get_absolute_url(self):
        return reverse('product:brand', args=[self.slug])

    def __str__(self):
        return self.title

    def image_tag(self):
        images = Image.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)
        if images.exists():
            return mark_safe('<img src="{}" height="50"/>'.format(images.first().image.url))
        return None


class Size(models.Model):
    name = models.CharField(max_length=300)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=300)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style ="background-color:{}">Color</p>'.format(self.code))
        return ""


class Attribute(models.Model):
    attribute = models.CharField(max_length=300)
    type = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.attribute}_{self.type}'


class CategoryProduct(MPTTModel):
    STATUS = (('True', 'True'), ('False', 'False'))
    title = models.CharField(max_length=300)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    status = models.CharField(max_length=15, choices=STATUS)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name_plural = "Products' Categories"

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        if self.parent:
            full_path = [self.title]
            k = self.parent
            while k is not None:
                full_path.append(k.title)
                k = k.parent
            return ' / '.join(full_path[::-1])
        else:
            return self.title

    def image_tag(self):
        images = Image.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)
        if images.exists():
            return mark_safe('<img src="{}" height="50"/>'.format(images.first().image.url))
        return None


class Products(models.Model):
    STATUS = (('True', 'True'), ('False', 'False'))
    VARIANTS = (('None', 'None'), ('Size', 'Size'), ('Color', 'Color'), ('Size-Color', 'Size-Color'),
                ('Brand-Size-Color', 'Brand-Size-Color'))
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    variant = models.CharField(max_length=30, choices=VARIANTS, default='None')
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=15, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="products")

    # like = models.ManyToManyField(CustomUser, through='Like', related_name='liked_item')
    # tags = TaggableManager()
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def image_tag(self):
        images = Image.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)
        if images.exists():
            return mark_safe('<img src="{}" height="50"/>'.format(images.first().image.url))
        return None


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products", null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, related_name="products", null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="products", null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="products", null=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="products",  null=True)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    def image_tag(self):
        images = Image.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)
        if images.exists():
            return mark_safe('<img src="{}" height="50"/>'.format(images.first().image.url))
        return None


