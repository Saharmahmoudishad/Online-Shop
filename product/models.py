from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel, TreeForeignKey

from core.models import Image


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


class CategoryProduct(MPTTModel):
    STATUS = (('True', 'True'), ('False', 'False'))
    title = models.CharField(max_length=300)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    status = models.CharField(max_length=15, choices=STATUS)
    image = models.ImageField(blank=True, upload_to='images/')
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
