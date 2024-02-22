from rest_framework import serializers
from core.models import Image, Province, City, DiscountCode, Comment


class ImageSerializer(serializers.ModelSerializer):
    image_tag = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'image', 'content_type', 'object_id', 'image_tag']

    def get_image_tag(self, obj):
        if obj.image:
            return obj.image_tag()
        return None


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'content_type', 'object_id', 'user', 'created', 'parent_comment', 'replies']
