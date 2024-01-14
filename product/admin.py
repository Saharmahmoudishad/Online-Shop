from django.contrib import admin

from product.models import Color, Size, CategoryProduct


class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ["title", "parent", "status", "image_tag", ]


class BrandAdmin(admin.ModelAdmin):
    list_display = ["title", "image_tag", ]


class SizeAdmin(admin.ModelAdmin):
    list_display = ["name", "code", ]


class ColorAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "color_tag", ]


admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
