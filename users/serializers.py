from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserAvatarSerializer(serializers.ModelSerializer):
    avatar_dataurl = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['avatar_dataurl']
        
class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'date_joined']
        
class UserPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(min_length = 8)
    new_password = serializers.CharField(min_length = 8)