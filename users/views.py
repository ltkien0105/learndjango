from django.shortcuts import render
from rest_framework.generics import ListAPIView, UpdateAPIView
from polls.serializers import PostSerializer, CommentSerializer, UserInfoSerializer
from polls.models import Post, Comment
from .models import User

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
    
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

class UserUpdateProfile(UpdateAPIView):
    serializer_class = UserInfoSerializer
    queryset = User.objects.all()
    
    def update(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        cloudinary.uploader.upload(request.data['avatarBase64'])
        # return super().update(request, *args, **kwargs)
    
