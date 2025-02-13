from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        
    def validate_email(self, value):
        if (User.objects.filter(email=value).exists()):
            raise serializers.ValidationError('A user with that email already exists', code='email_unique')
        
        return value
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']