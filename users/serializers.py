from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            address=validated_data.get('address', ''),
            phone_number=validated_data.get('phone_number', ''),
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    
    def validate(self, data):
        required_fields = ['username', 'email', 'password']  # Adjust based on your actual required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise serializers.ValidationError({
                'missing_fields': f"Missing required fields: {', '.join(missing_fields)}"
            })
        return data
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        required_fields = ['email', 'password']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise serializers.ValidationError({
                'missing_fields': f"Missing required fields: {', '.join(missing_fields)}"
            })
        return data
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'role', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'role']
