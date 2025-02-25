from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.pagination import PageNumberPagination
from ..serializers import PostSerializer, CommentSerializer
from ..models import Post, UserLike, Comment
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Count, OuterRef, Exists
from django.contrib.auth import get_user_model

User = get_user_model()

class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        user = self.request.user
        if category_id:
            if (user.id):
                return Post.objects.filter(category_id=category_id).annotate(liked=Exists(UserLike.objects.filter(user=user.id, post=OuterRef('id'))))
            return Post.objects.filter(category_id=category_id)

        if (user.id):
            return Post.objects.annotate(liked=Exists(UserLike.objects.filter(user=user.id, post=OuterRef('id')))).all()
        return Post.objects.all()
    
    def post(self, request, *args, **kwargs):
        self.authentication_classes = [SessionAuthentication]
        self.permission_classes = [IsAuthenticated]
        return super().post(request, *args, **kwargs)
    
class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        if (self.request.user.id):
            return Post.objects.annotate(comment_count=Count('comments'), liked=Exists(UserLike.objects.filter(user=self.request.user.id, post=OuterRef('id'))))
        return Post.objects.annotate(comment_count=Count('comments'))
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def update(self, request, *args, **kwargs):
        self.authentication_classes = [SessionAuthentication]
        self.permission_classes = [IsAuthenticated]
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        self.authentication_classes = [SessionAuthentication]
        self.permission_classes = [IsAuthenticated]
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)
    
class PostUpdateLikeCount(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        action = request.data.get("action")  # 'like' or 'unlike'
        user_id = request.data.get("user_id")  # 'like' or 'unlike'
        
        if action == "like":
            post.likes += 1
            UserLike.objects.create(user=User.objects.get(pk=user_id), post=post)
        elif action == "unlike":
            post.likes = max(0, post.likes - 1)  # Prevent negative likes
            user_like = UserLike.objects.get(user=user_id, post=pk)
            user_like.delete()
        else:
            return Response({"error": "Invalid action"}, status=HTTP_400_BAD_REQUEST)
        
        post.save(update_fields=['likes'])
        return Response({"likes": post.likes}, status=HTTP_200_OK)
    
class PostGetComments(APIView):
    def get(self, request, pk):
        order = request.query_params.get('order')
        if (order):
            if (order == "asc"):
                comments = Comment.objects.filter(post=pk).order_by("created_at")
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data, status=HTTP_200_OK)
            elif (order == "desc"):
                comments = Comment.objects.filter(post=pk).order_by("-created_at")
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                return Response("Invalid order", status=HTTP_400_BAD_REQUEST)
        
        comments = Comment.objects.filter(post=pk).order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
class PostSearch(APIView, PageNumberPagination):
    page_size_query_param = 'page_size'
    
    def get(self, request):
        query = request.query_params.get('q', '')
        posts = Post.objects.filter(title__icontains=query)
        paginated_posts = self.paginate_queryset(posts, request)
        serializer = PostSerializer(paginated_posts, many=True)
        return self.get_paginated_response(serializer.data)
        
    
