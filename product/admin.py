from django.contrib import admin

from product.models import Color, Size


# Register your models here.
class SizeAdmin(admin.ModelAdmin):
    list_display = ["name", "code", ]


class ColorAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "color_tag", ]


admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
