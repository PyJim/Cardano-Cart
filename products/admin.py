from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = Product.images.through  # Use the through model for the many-to-many relationship
    extra = 1  # Allows you to add one image by default

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]  # Include the inline for images

    list_display = ('name', 'seller', 'price', 'stock', 'category', 'created_at')  # Display these fields in the admin list view
    search_fields = ('name', 'category')  # Add search functionality by name and category

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image',)  # Display the image field in the admin list view

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)