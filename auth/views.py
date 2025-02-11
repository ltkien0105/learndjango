from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SignUpSerializer, LoginSerializer

class SignUp(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"status": True, "message": "Sign up successfully"}, status.HTTP_201_CREATED)
        else:
            return Response({"status": False, "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if (serializer.is_valid()):
            print(serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        