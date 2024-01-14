from django.db import models

from django.utils.safestring import mark_safe


class Size(models.Model):
    name = models.CharField(max_length=300)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=300)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style ="background-color:{}">Color</p>'.format(self.code))
        return ""
