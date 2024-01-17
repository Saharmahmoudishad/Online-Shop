from django.contrib import admin
from .models import *


class ImageAdmin(admin.ModelAdmin):
    list_display = ["image", "image_tag", ]


admin.site.register(Image, ImageAdmin)
admin.site.register(Comment)
