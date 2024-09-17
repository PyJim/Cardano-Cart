from rest_framework import serializers
from products.models import Product
from users.models import CustomUser
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    
    class Meta:
        model = Review
        fields = ['user', 'rating', 'comment', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Access the current user from the context
        user = self.context['request'].user
        product = self.context['product']  # Get product from context

        # Create the review with the product from the URL
        review = Review.objects.create(user=user, product=product, **validated_data)
        return review

    def validate(self, data):
        required_fields = ['rating', 'comment']
        # Check if required fields are present
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise serializers.ValidationError({
                'missing_fields': f"Missing required fields: {', '.join(missing_fields)}"
            })
        return data
