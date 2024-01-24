from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from core.mixins import SoftDeleteMixin
from core.models import Image
from customers.models import CustomUser
from translated_fields import TranslatedField as translate
from django.utils.translation import gettext_lazy as _


class Brand(SoftDeleteMixin):
    title = models.CharField(max_length=300, verbose_name=_("Title"), unique=True)
    slug = models.SlugField(max_length=300,null=True, blank=True, verbose_name=_("slug"))

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def get_absolute_url(self):
        return reverse('product:brand', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def image_tag(self, width=120, height=120):
        images = Image.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)
        if images.exists():
            return mark_safe('<img src="{}" width="{}" height="{}" />'.format(images.first().image.url, width, height))
        return None


class Size(SoftDeleteMixin):
    gender = models.CharField(max_length=300, verbose_name=_("gender"), )
    code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("code"))

    class Meta:
        verbose_name = _('Size')
        verbose_name_plural = _('Size')

    def __str__(self):
        return self.code


class Material(SoftDeleteMixin):
    name = models.CharField(max_length=300, verbose_name=_("name"), unique=True)

    class Meta:
        verbose_name = _('Material')
        verbose_name_plural = _('Material')

    def __str__(self):
        return self.name


class Color(SoftDeleteMixin):
    name = models.CharField(max_length=300, verbose_name=_("name"), unique=True)
    code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("code"))

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Color')

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style ="background-color:{}">Color</p>'.format(self.code))
        return ""


class Attribute(SoftDeleteMixin):
    attribute = models.CharField(max_length=300, verbose_name=_("attribute"))
    type = models.CharField(max_length=300, verbose_name=_("type"))

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attribute')

    def __str__(self):
        return f'{self.attribute}_{self.type}'


class CategoryProduct(MPTTModel, SoftDeleteMixin):
    STATUS = (('True', 'True'), ('False', 'False'))
    title = models.CharField(max_length=300, verbose_name=_("title"))
    slug = models.SlugField(null=True, blank=True, verbose_name=_("slug"))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name=_("parent"))
    status = models.CharField(max_length=15, choices=STATUS, verbose_name=_("status"))
    tags = TaggableManager()
    description = models.TextField(max_length=255, verbose_name=_("description"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("updated"))

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _("Products Categories")

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

    def image_tag(self, width=120, height=120):
        images = Image.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)
        if images.exists():
            return mark_safe('<img src="{}" width="{}" height="{}" />'.format(images.first().image.url, width, height))
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Products(SoftDeleteMixin):
    STATUS = (('True', 'True'), ('False', 'False'))
    VARIANTS = (('None', 'None'), ('Size', 'Size'), ('Color', 'Color'),
                ('Size-Color', 'Size-Color'),
                ('Size-Color-material', 'Size-Color_material'), ('Size-Color', 'Size-Color'))
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name="products",
                                 verbose_name=_("category"))
    title = models.CharField(max_length=150, verbose_name=_("title"))
    tags = TaggableManager()
    description = models.TextField(verbose_name=_("description"))
    price = models.FloatField(default=0, verbose_name=_("price"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("quantity"))
    variant = models.CharField(max_length=30, choices=VARIANTS, default='None', verbose_name=_("variant"))
    detail = RichTextUploadingField(verbose_name=_("detail"))
    slug = models.SlugField(null=True, blank=True, verbose_name=_("slug"))
    status = models.CharField(max_length=15, choices=STATUS, verbose_name=_("status"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("updated"))
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="products",
                             verbose_name=_("user"))

    # like = models.ManyToManyField(CustomUser, through='Like', related_name='liked_item')
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse('product:product_detail', kwargs={'slug': self.slug})

    def image_tag(self, width=120, height=120):
        images = Image.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)
        if images.exists():
            return mark_safe('<img src="{}" width="{}" height="{}" />'.format(images.first().image.url, width, height))
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Variants(SoftDeleteMixin):
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("title"))
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="Variants", verbose_name=_("product"))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="Variants", null=True,
                              verbose_name=_("brand"))
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, related_name="Variants", null=True,
                             verbose_name=_("size"))
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="Variants", null=True,
                              verbose_name=_("color"))
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="Variants", null=True,
                                 verbose_name=_("material"))
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="Variants", null=True,blank=True,
                                  verbose_name=_("attribute"))
    price = models.PositiveIntegerField(default=0, verbose_name=_("price"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("quantity"))

    class Meta:
        verbose_name = _('Variant')
        verbose_name_plural = "Variants"

    def __str__(self):
        return self.title

    def image_tag(self, width=120, height=120):
        images = Image.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)
        if images.exists():
            return mark_safe('<img src="{}" width="{}" height="{}" />'.format(images.first().image.url, width, height))
        return None


class DiscountProduct(SoftDeleteMixin):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_("Product"))
    deadline = models.DateTimeField(verbose_name=_("Deadline"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))

    class Meta:
        verbose_name = _('Discount Product')
        verbose_name_plural = _("Discount Products")

    def __str__(self):
        return f'{self.title}_{self.amount}'
