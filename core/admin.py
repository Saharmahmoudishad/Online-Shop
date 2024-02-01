from django.contrib import admin
from .models import *


class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "created", "content_type", "parent_comment",]
    raw_id_fields =("user","parent_comment",)


class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "image_tag", ]


class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ["title", "amount", "deadline", ]


admin.site.register(Image, ImageAdmin)
admin.site.register(Comment)
admin.site.register(DiscountCode, DiscountCodeAdmin)
