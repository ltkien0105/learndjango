from rest_framework import serializers
from .models import Category, Thread, Post
from django.contrib.auth import get_user_model
User = get_user_model()

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    thread_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'description', 'thread_count']
        
class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all(), write_only=True)
    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'thread']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserInfoSerializer(instance.user).data
        representation['thread'] = instance.thread.id
        return representation
        
class ThreadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'category', 'user', 'posts']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['user'] = UserInfoSerializer(instance.user).data
        return representation
    