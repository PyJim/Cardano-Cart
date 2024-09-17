# cart/serializers.py
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def create(self, validated_data):
        product = validated_data.get('product')
        if not product:
            raise serializers.ValidationError({'product': 'Product not found'})
        cart_item = CartItem.objects.create(product=product, **validated_data)
        return cart_item

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method not in ['PUT']:
            required_fields = ['quantity', 'product']  # Use 'product' instead of 'product_id'
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                raise serializers.ValidationError({
                    'missing_fields': f"Missing required fields: {', '.join(missing_fields)}"
                })
        return data


