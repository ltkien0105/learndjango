from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from django.db.models import Count

from .serializers import CategorySerializer, ThreadSerializer, PostSerializer
from .models import Category, Thread, Post

class Categories(ListCreateAPIView):
    serializer_class = CategorySerializer
    def get_queryset(self):
        category_id = self.kwargs.get('id', None)
        is_get_thread_count = self.request.query_params.get('thread_count')
        if category_id:
            return Category.objects.filter(pk=category_id)
        if is_get_thread_count and is_get_thread_count == '1':
            return Category.objects.annotate(thread_count=Count('thread'))

        return Category.objects.all()
    
class Threads(ListCreateAPIView):
    serializer_class = ThreadSerializer
    
    def get_queryset(self):
        thread_id = self.kwargs.get('id', None)
        category_id = self.request.query_params.get('category_id')
        if thread_id:
            return Thread.objects.filter(id=thread_id)
        if category_id:
            return Thread.objects.filter(category_id=category_id)

        return Thread.objects.all()

class Posts(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get('id', None)
        thread_id = self.request.query_params.get('thread')
        if post_id:
            return Post.objects.filter(pk=post_id)
        if thread_id:
            return Post.objects.filter(thread_id=thread_id)

        return Post.objects.all()