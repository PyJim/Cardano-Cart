from rest_framework import serializers
from .models import Order, OrderItem  # Import Cart, CartItem, and Product models
from products.serializers import ProductSerializer  # Assuming a Product serializer exists
from cart.models import CartItem
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nested product serializer

    class Meta:
        model = CartItem  # Using CartItem since it's similar to an order item
        fields = ['product', 'quantity', 'get_total_item_price']  # Include price calculation

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source='buyer.carts.items', many=True, read_only=True)
    buyer = serializers.StringRelatedField(read_only=True)  # Display the buyer's username or email

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'shipping_address', 'total_amount', 'status', 'tracking_number', 'created_at', 'updated_at', 'order_items']
        read_only_fields = ['id', 'buyer', 'total_amount', 'created_at', 'updated_at', 'order_items']

    def create(self, validated_data):
        # Get cart from the context, ensure it's tied to the current user
        cart = self.context['cart']
        buyer = self.context['request'].user

        # Create the order
        order = Order.objects.create(
            buyer=buyer,
            shipping_address=validated_data['shipping_address'],
            total_amount=cart.total_price,  # Use the total price from the cart
            status='pending',
            tracking_number=validated_data.get('tracking_number', '')
        )

        # Create OrderItems from CartItems
        for cart_item in cart.items.all():
            # Create OrderItems manually
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

        return order
