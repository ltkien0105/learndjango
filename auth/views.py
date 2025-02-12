from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from .serializers import SignUpSerializer, LoginSerializer, UserInfoSerializer

class SignUp(APIView):
    def post(self, request):
        try:
            serializer = SignUpSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return Response({"status": True, "message": "Sign up successfully"}, status.HTTP_201_CREATED)
            else:
                return Response({"status": False, "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        except ParseError:
            return Response({"status": False, "errors": "Invalid JSON"}, status.HTTP_400_BAD_REQUEST)
        
class Login(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if (serializer.is_valid()):
                user = authenticate(request=request, username=serializer.validated_data.get('username'), password=serializer.validated_data.get('password'))
                
                if not user:
                    raise AuthenticationFailed
                
                response = Response({"status": True, "message": "Login successfully", "data": {
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }}, status=status.HTTP_200_OK)
                access, refresh = get_token(user)
                response.set_cookie('access_token', value=access, secure=True, httponly=True, samesite='none')
                response.set_cookie('refresh_token', value=refresh, secure=True, httponly=True, samesite='none')
                return response
            else:
                return Response({"status": False, "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed:
            return Response({"status": False, "errors": "Invalid username or password"}, status.HTTP_401_UNAUTHORIZED)
        except ParseError:
            return Response({"status": False, "errors": "Invalid JSON"}, status.HTTP_400_BAD_REQUEST)

class UserInfo(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer
    
    def get_object(self):
        return self.request.user

def get_token(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return (access_token, str(refresh))
