from rest_framework import serializers

from product.models import Products, Variants


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class VariantsSerializer(serializers.ModelSerializer):
    image_tag = serializers.SerializerMethodField()
    class Meta:
        model = Variants
        fields = ["id", "title", "product", "brand", "size", "color", "material", "attribute","image_tag"]

    def get_image_tag(self, instance):
        # Access the image_tag method of the Variants instance
        return instance.image_tag()