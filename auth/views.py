from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError, AuthenticationFailed
from rest_framework.authentication import SessionAuthentication

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from .serializers import SignUpSerializer, LoginSerializer, UserInfoSerializer

class SetCsrfToken(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, _):
        return Response('CSRF cookie set')
    
class Login(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if (serializer.is_valid()):
                user = authenticate(request=request, username=serializer.validated_data.get('username'), password=serializer.validated_data.get('password'))
                if not user:
                    raise AuthenticationFailed
                
                login(request, user)
                user_serializer = UserInfoSerializer(user)
                return Response({"status": True, "message": "Login successfully", "data": user_serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, "message": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed:
            return Response({"status": False, "message": "Invalid username or password"}, status.HTTP_401_UNAUTHORIZED)
        except ParseError:
            return Response({"status": False, "message": "Invalid JSON"}, status.HTTP_400_BAD_REQUEST)
        
class Logout(APIView):
    def post(self, request):
        logout(request)
        
        return Response({"message": "Successfully logged out!"}, status=status.HTTP_200_OK)
     
class UserInfo(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    serializer_class = UserInfoSerializer
    
    def get(self, request):
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            serializer = UserInfoSerializer(request.user)
            return Response(serializer.data)
        
        return Response({"status": False, "message": "Not logged in"}, status=status.HTTP_200_OK)
    
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

