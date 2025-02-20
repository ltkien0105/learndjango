from rest_framework import serializers
from .models import Category, Comment, Post
from django.contrib.auth import get_user_model
User = get_user_model()

class UserInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'avatar']

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'description', 'post_count']
        
class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'post']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserInfoSerializer(instance.user).data
        representation['post'] = instance.post.id
        return representation
        
class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'category', 'user', 'comments']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['user'] = UserInfoSerializer(instance.user).data
        return representation
    