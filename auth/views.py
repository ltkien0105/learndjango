from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken

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
                    "id": user.id,
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
        
class Logout(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as e:
                return Response({"error":"Error invalidating token:" + str(e) }, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response({"message": "Successfully logged out!"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        
        return response    
        

class UserInfo(RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    
    def get_object(self):
        return self.request.user
    
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request):
        
        refresh_token = request.COOKIES.get("refresh_token")
        
        if not refresh_token:
            return Response({"error":"Refresh token not provided"}, status= status.HTTP_401_UNAUTHORIZED)
    
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            response = Response({"message": "Access token token refreshed successfully"}, status=status.HTTP_200_OK)
            response.set_cookie(key="access_token", 
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="None")
            return response
        except InvalidToken:
            return Response({"error":"Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

def get_token(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return (access_token, str(refresh))
