from rest_framework import serializers

from decimal import Decimal
from .models import Product, Collection, Review, Cart, CartItem

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # featured_product = serializers.PrimaryKeyRelatedField(
    #     read_only=True

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # description = serializers.CharField()
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    # Fetch related Collection object
    # 1. Primary key:: This will return Collection IDs only
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())

    # 2. String:: This will return Collection Titles (1000 extra SQL queries)
    # collection = serializers.StringRelatedField()

    # 3. Nested Object:: This will return Nested Collection object (1 extra SQL query)
    # collection = CollectionSerializer()

    # 4. Hyperlink:: Return Hyper Links
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def calculate_tax(self, product : Product):
        return product.unit_price * Decimal('1.1')

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # instance.unit_price = validated_data.get('unit_price')
        # instance.save()
        # return instance
        return super().update(instance, validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id= product_id, **validated_data)

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Cart
        fields = ['id']