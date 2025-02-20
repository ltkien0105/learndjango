from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from polls.serializers import PostSerializer, CommentSerializer
from polls.models import Post, Comment
from .models import User

from .serializers import UserAvatarSerializer, UserProfileSerializer

from dotenv import load_dotenv
import os
load_dotenv()

import cloudinary
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
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
        
class UserUpdateAvatar(UpdateAPIView):
    serializer_class=UserAvatarSerializer
    queryset = User.objects.all()
    
    def update(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(pk=user_id)
        uploadResult = cloudinary.uploader.upload(
            request.data['avatar_dataurl'],
            folder = 'avatars',
            public_id = f"avatar_{user.username}",
            transformation=[
                {"width": 100, "height": 100, "crop": "crop"},
                {"width": 100, "height": 100, "crop": "fill"}
            ]
        )
        user.avatar = uploadResult['secure_url']
        user.save()
        
        return Response({'status': True, 'message': 'Update avatar successfully', 'data': {'secure_url': uploadResult['secure_url']} }, status=HTTP_200_OK)
    
                

    
