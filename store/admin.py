from django.contrib import admin
from . import models
# from .models import Product, Collection

# Register Models for Admin Site

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price']
    list_editable = ['unit_price']
    list_per_page = 15
    search_fields = ['title']

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 15
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']

# admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Collection)
# admin.site.register(models.Customer)