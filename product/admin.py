from django.contrib import admin

from product.models import Color, Size, CategoryProduct, Brand, Material, Attribute, Products, Variants


class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "parent", "status", "image_tag", ]
    search_field = ["title", ]
    list_filter = ["parent", ]


class BrandAdmin(admin.ModelAdmin):
    list_display = ["title", "image_tag", ]
    search_field = ["title", ]


class SizeAdmin(admin.ModelAdmin):
    list_display = ["gender", "code", ]
    search_field = ["code", ]
    list_filter = ["gender", ]


class ColorAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "color_tag", ]
    search_field = ["name", "code", ]


class MaterialAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    search_field = ["name", ]


class AttributeAdmin(admin.ModelAdmin):
    list_display = ["attribute", "type", ]
    search_field = ["attribute", ]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "image_tag", ]
    search_field = ["category", "title", ]
    list_filter = ["category", "quantity"]


class VariantsAdmin(admin.ModelAdmin):
    list_display = ["title", "color", "size", "brand", "material", "attribute", "price", "quantity",]
    search_field = ["product", ]
    list_filter = ["product", "title", "quantity"]


class DiscountProductAdmin(admin.ModelAdmin):
    list_display = ["title", "product", "time",]
    list_filter = ["title",]


admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Products, ProductAdmin)
admin.site.register(Variants, VariantsAdmin)
