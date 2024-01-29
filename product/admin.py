from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from product.models import Color, Size, CategoryProduct, Brand, Material, Attribute, Products, Variants, \
    DiscountProduct, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ProductInline(admin.TabularInline):
    model = Products
    readonly_fields = ('id',)
    extra = 1


class CategoryProductAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count', "status", "image_tag",)
    list_display_links = ('indented_title',)
    inlines = [ProductInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        qs = CategoryProduct.objects.add_related_count(
            qs,
            Products,
            'category',
            'products_cumulative_count',
            cumulative=True)

        qs = CategoryProduct.objects.add_related_count(qs,
                                                       Products,
                                                       'category',
                                                       'products_count',
                                                       cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'Related products (in tree)'


class BrandAdmin(admin.ModelAdmin):
    list_display = ["title", "image_tag", ]
    search_fields = ["title", ]


class SizeAdmin(admin.ModelAdmin):
    list_display = ["gender", "code", ]
    search_fields = ["code", ]
    list_filter = ["gender", ]


class ColorAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "color_tag", ]
    search_fields = ["name", "code", ]


class MaterialAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    search_fields = ["name", ]


class AttributeAdmin(admin.ModelAdmin):
    list_display = ["attribute", "type", ]
    search_fields = ["attribute", ]


class VariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('id',)
    extra = 1



class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "image_tag", ]
    search_fields = ["category__title", "title", ]
    list_filter = ["category", "quantity"]
    inlines = [VariantsInline,]


class VariantsAdmin(admin.ModelAdmin):
    list_display = ["title", "color", "size", "brand", "material", "attribute", "price", "quantity", ]
    search_fields = ["product__title", 'brand__name']
    list_filter = ["product", "title", "quantity"]


class DiscountProductAdmin(admin.ModelAdmin):
    list_display = ["title", "product", "deadline", "amount", ]
    list_filter = ["title", ]


admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Products, ProductAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(DiscountProduct, DiscountProductAdmin)
