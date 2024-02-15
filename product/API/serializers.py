from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from core.API.serializers import ImageSerializer
from core.models import Image
from product.models import Products, Variants


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class VariantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variants
        fields = ["id", "title", "product", "brand", "size", "color", "material", "attribute"]
