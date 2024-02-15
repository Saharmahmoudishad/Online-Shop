from django.contrib import admin

from customers.models import Address
from .models import *


class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "created", "content_type", "parent_comment", ]
    raw_id_fields = ("user", "parent_comment",)


class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "image_tag", ]


class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ["title", "amount", "deadline", ]


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class CityAdmin(admin.ModelAdmin):
    inlines = [AddressInline]


class CityInline(admin.TabularInline):
    model = City
    extra = 1


class ProvinceAdmin(admin.ModelAdmin):
    inlines = [CityInline]


admin.site.register(Image, ImageAdmin)
admin.site.register(Comment)
admin.site.register(DiscountCode, DiscountCodeAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Province, ProvinceAdmin)
