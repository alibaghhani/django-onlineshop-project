from rest_framework import serializers
from account.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """
    serializer for address model
    """
    class Meta:
        model = Address
        fields = '__all__'
