from rest_framework import serializers

from products.models import Product
from .models import Order, OrderItem  # Import Order and OrderItem models
from products.serializers import ProductSerializer  # Assuming a Product serializer exists
from cart.models import CartItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Use PrimaryKeyRelatedField to include only product ID

    class Meta:
        model = OrderItem  # Use the correct model (OrderItem)
        fields = ['product', 'quantity', 'price']  # Include 'price' which stores the final price of the item


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    buyer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'shipping_address', 'total_amount', 'status', 'tracking_number', 'created_at', 'updated_at', 'order_items']
        read_only_fields = ['id', 'buyer', 'total_amount', 'created_at', 'updated_at', 'order_items']

    def create(self, validated_data):
        # Get cart from the context, ensure it's tied to the current user
        cart = self.context['cart']
        buyer = self.context['request'].user

        # Calculate total amount from the cart
        total_amount = sum(cart_item.quantity * cart_item.product.price for cart_item in cart.items.all())

        # Create the order
        order = Order.objects.create(
            buyer=buyer,
            shipping_address=validated_data['shipping_address'],
            total_amount=total_amount,
            status='pending',
            tracking_number=validated_data.get('tracking_number', '')
        )

        # Create OrderItems from CartItems
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price * cart_item.quantity  # Set the price based on product price and quantity
            )

        return order
