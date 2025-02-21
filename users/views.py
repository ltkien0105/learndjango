from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from polls.serializers import PostSerializer, CommentSerializer
from polls.models import Post, Comment
from .models import User

from django.contrib.auth import authenticate

from .serializers import UserAvatarSerializer, UserProfileSerializer, UserPasswordSerializer

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

class UserRetrieveUpdateProfile(RetrieveUpdateAPIView):
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
    
class UserChangePassword(UpdateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class=UserPasswordSerializer
    queryset = User.objects.all()
    
    def update(self, request, *args, **kwargs):
        serializer = UserPasswordSerializer(data=request.data)
        if (serializer.is_valid()):
            user_id = kwargs.get('pk')
            user = User.objects.get(pk=user_id)
            user = authenticate(request, username = user.username, password = serializer.validated_data.get('current_password'))
            if user:
                user.set_password(serializer.validated_data.get('new_password'))
                user.save()
                return Response({'status': True, 'message': 'Change password successfully'}, status=HTTP_200_OK)
            else:
                return Response({'status': False, 'message': 'Current password is incorrect'}, status=HTTP_200_OK)
        else:
            return Response({"status": False, "errors": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
    
                

    
