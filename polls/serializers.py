from rest_framework import serializers
from .models import Category, Thread

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    thread_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'description', 'thread_count']
        
class ThreadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    category = serializers.SerializerMethodField()
    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'category', 'user']
        
    def get_category(self, thread):
        return CategorySerializer(thread.category).data