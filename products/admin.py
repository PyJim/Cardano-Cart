from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'price', 'stock', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'category', 'seller__username')
    list_filter = ('category', 'created_at', 'updated_at')

