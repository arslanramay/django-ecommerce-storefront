from rest_framework import serializers
from django.db import transaction
from decimal import Decimal
from .models import Product, Collection, Customer, Order, OrderItem, Review, Cart, CartItem

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


# CART SERIALIZERS
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item:CartItem):
        return cart_item.product.unit_price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True) # This will return a list of CartItem objects
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart:Cart):
        # [item for item in  cart.items.all()]
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    # Validate the product_id field. 'value' is the product_id value
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    # user_id = serializers.IntegerField(source='user.id')

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

    # def validate_payment_status(self, value):
    #     if value not in [Order.PAYMENT_PENDING, Order.PAYMENT_COMPLETE]:
    #         raise serializers.ValidationError('Invalid payment status.')
    #     return value

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    # Validate the cart_id to check if Cart exists and is not empty
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the given ID.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        cart_id = self.validated_data['cart_id']
        user_id = self.context['user_id']

        print(cart_id)
        print(user_id)

         # Wrap the entire order creation in a transaction block
        with transaction.atomic():
            # Get the customer instance associated with the user
            customer = Customer.objects.get(user_id=user_id)
            # (customer, created) = Customer.objects.get_or_create(user_id=user_id)

            # Create a new order for the customer
            order = Order.objects.create(customer=customer)
            # order = Order.objects.create(customer=customer[0], payment_status=Order.PAYMENT_PENDING)

            # Retrieve all cart items and join with related product in one query
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

            # Create OrderItem instances for each cart item
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.unit_price
                )
                for item in cart_items
            ]

            # Insert all order items in a single query
            OrderItem.objects.bulk_create(order_items)

            # Delete the cart after converting it to an order
            Cart.objects.filter(pk=cart_id).delete()

            # Return the created order object
            return order