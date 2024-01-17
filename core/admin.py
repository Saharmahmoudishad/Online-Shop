from django.contrib import admin
from .models import *


class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "image_tag", ]


class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ["title", "amount", "deadline", ]


admin.site.register(Image, ImageAdmin)
admin.site.register(Comment)
admin.site.register(DiscountCode, DiscountCodeAdmin)
