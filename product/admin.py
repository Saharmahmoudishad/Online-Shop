from django.contrib import admin

from product.models import Color, Size, CategoryProduct, Brand, Material, Attribute, Products


class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ["title", "parent", "status", "image_tag", ]


class BrandAdmin(admin.ModelAdmin):
    list_display = ["title", "image_tag", ]


class SizeAdmin(admin.ModelAdmin):
    list_display = ["name", "code", ]


class ColorAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "color_tag", ]


class MaterialAdmin(admin.ModelAdmin):
    list_display = ["name", ]


class AttributeAdmin(admin.ModelAdmin):
    list_display = ["attribute", "type", ]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "image_tag", ]


class VariantsAdmin(admin.ModelAdmin):
    list_display = ["title", "color", "size", "brand", "material", "attribute", "price", "quantity", "image_tag", ]


admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Products, ProductAdmin)
