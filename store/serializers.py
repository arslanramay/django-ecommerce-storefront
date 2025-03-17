from rest_framework import serializers

from decimal import Decimal
from .models import Product, Collection

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    # featured_product = serializers.PrimaryKeyRelatedField(
    #     read_only=True

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')
    # Fetch related Collection object
    # This will return Collection IDs only
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )
    # This will return Collection Titles (1000 extra SQL queries)
    # collection = serializers.StringRelatedField()
    # This will return Nested Collection object (1 extra SQL query)
    collection = CollectionSerializer()

    def get_price_with_tax(self, product : Product):
        return product.unit_price * Decimal('1.1')