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
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']