from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
# from .models import Product, Collection

# Register Models for Admin Site
# Product Admin
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 15
    search_fields = ['title']
    list_select_related = ['collection']

    # Add custom method to display collection title(computed field)
    def collection_title(self, product):
        return product.collection.title

    # Add custom method to display inventory status(computed field)
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

# Collection Admin
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )

# Customer Admin
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership'] # Override this in Customer Model
    list_editable = ['membership']
    list_per_page = 15
    list_select_related = ['user'] # Eager load users to reduce the number of queries
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name', 'last_name']

# Order Admin
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']

# admin.site.register(models.Product, ProductAdmin)
# admin.site.register(models.Collection)
# admin.site.register(models.Order)
# admin.site.register(models.Customer)