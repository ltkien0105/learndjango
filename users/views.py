from django.shortcuts import render
from rest_framework.generics import ListAPIView
from polls.serializers import PostSerializer, CommentSerializer
from polls.models import Post, Comment

from dotenv import load_dotenv
import os
load_dotenv()

import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api

class UserPosts(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Post.objects.filter(user=user_id)
        return queryset
    
class UserComments(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Comment.objects.filter(user=user_id)
        return queryset
    
class UserImagePreview():
    pass
    
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)
