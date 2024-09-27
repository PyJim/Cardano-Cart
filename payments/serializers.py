from rest_framework import serializers
from orders.models import Order  # Make sure to import your Order model

class PaymentVerificationSerializer(serializers.Serializer):
    transaction_id = serializers.CharField()

    class Meta:
        fields = ['transaction_id']

    def validate(self, data):
        transaction_id = data.get('transaction_id')
        order = self.context['order']  # Get the order from context

        # Check if the order exists and is valid
        if not order:
            raise serializers.ValidationError({"order": "Order does not exist."})

        # Check if transaction_id is present
        if not transaction_id:
            raise serializers.ValidationError({"transaction_id": "Transaction ID is required."})

        # Access the order from context
        data['seller_address'] = order.product.seller.wallet_id  # Set seller_address
        data['expected_amount'] = order.total_amount  # Set expected_amount

        return data
