from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.db import models
from core.mixins import SoftDeleteMixin


class Comment(SoftDeleteMixin):
    content = models.TextField(verbose_name=_("Content"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name=_("object id"))
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey("customers.CustomUser", on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"),)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _("Comments")


class Image(SoftDeleteMixin):
    image = models.ImageField(upload_to='images/', verbose_name=_("image"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name=_("object id"))
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _("Images")

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="50" />'.format(self.image.url))
        return ''

    image_tag.short_description = 'Image Preview'


class Province(SoftDeleteMixin):
    name = models.CharField(max_length=40, verbose_name=_("Province Name"))

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _("Provinces")


class City(SoftDeleteMixin):
    name = models.CharField(max_length=40, verbose_name=_("City Name"))
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_("Province"), default="0")

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _("Cites")


class DiscountCode(SoftDeleteMixin):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    deadline = models.DateTimeField(verbose_name=_("Deadline"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name=_("Object ID"))
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('Discount')
        verbose_name_plural = _("Discounts")

    def __str__(self):
        return f'{self.title}_{self.amount}'
