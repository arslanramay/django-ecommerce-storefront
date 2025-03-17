from rest_framework import serializers

from decimal import Decimal
from .models import Product, Collection

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # featured_product = serializers.PrimaryKeyRelatedField(
    #     read_only=True

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # description = serializers.CharField()
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')

    # Fetch related Collection object
    # 1. Primary key:: This will return Collection IDs only
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )
    # 2. String:: This will return Collection Titles (1000 extra SQL queries)
    # collection = serializers.StringRelatedField()
    # 3. Nested Object:: This will return Nested Collection object (1 extra SQL query)
    # collection = CollectionSerializer()
    # 4. Hyperlink:: Return Hyper Links
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail'
    )

    def get_price_with_tax(self, product : Product):
        return product.unit_price * Decimal('1.1')