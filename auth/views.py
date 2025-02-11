from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import AuthenticationFailed

from .serializers import SignUpSerializer, LoginSerializer

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
                return Response({"status": True, "message": "Login successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed:
            return Response({"status": False, "errors": "Invalid username or password"}, status.HTTP_401_UNAUTHORIZED)
        except ParseError:
            return Response({"status": False, "errors": "Invalid JSON"}, status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    pass
        