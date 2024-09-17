# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)
    unit_price = serializers.SerializerMethodField()  # Add unit_price as a read-only field

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'unit_price']  # Include unit_price in fields

    def get_unit_price(self, obj):
        # Return the price of the product associated with this cart item
        if obj.product:
            return obj.product.price  # Adjust according to your Product model's price field
        return None

    def create(self, validated_data):
        product = validated_data.get('product')
        if not product:
            raise serializers.ValidationError({'product': 'Product not found'})
        unit_price = product.price  # Retrieve the product's price
        cart_item = CartItem.objects.create(product=product, unit_price=unit_price, **validated_data)
        return cart_item

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method not in ['PUT']:
            required_fields = ['quantity', 'product']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                raise serializers.ValidationError({
                    'missing_fields': f"Missing required fields: {', '.join(missing_fields)}"
                })
        return data
