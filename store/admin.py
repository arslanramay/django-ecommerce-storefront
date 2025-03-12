from django.contrib import admin
from . import models
# from .models import Product, Collection

# Register Models for Admin Site

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

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 15
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']

# admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Collection)
# admin.site.register(models.Order)
# admin.site.register(models.Customer)