from rest_framework import serializers

from customers.models import Address, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phonenumber', 'email', 'firstname', 'lastname', 'how_know_us', 'created', 'updated', 'is_active', 'is_admin', 'group', 'password']
        read_only_fields = ['created', 'updated']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'