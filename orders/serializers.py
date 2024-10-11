from rest_framework import serializers
from products.models import Product
from .models import Order  # Import Order model
from products.serializers import ProductSerializer  # Assuming a Product serializer exists

class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Reference to a single product
    buyer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'product', 'shipping_address', 'total_amount', 'status', 'tracking_number', 'created_at', 'updated_at']
        read_only_fields = ['id', 'buyer', 'total_amount', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Get the current user as the buyer
        buyer = self.context['request'].user

        # Get the selected product
        product = validated_data['product']

        # Calculate the total amount based on the product price and quantity (assuming 1 item)
        total_amount = product.price

        # Create the order
        order = Order.objects.create(
            buyer=buyer,
            product=product,
            shipping_address=validated_data['shipping_address'],
            total_amount=total_amount,
            status='pending',
            tracking_number=validated_data.get('tracking_number', '')
        )

        return order

    def to_representation(self, instance):
        # Call the parent method to get the default representation
        representation = super().to_representation(instance)

        # Pass the request context to the product serializer
        product_context = self.context.copy()
        product_context['request'] = self.context['request']  # Make sure the request is included

        # Update the product representation with the new context
        representation['product'] = ProductSerializer(instance.product, context=product_context).data

        return representation