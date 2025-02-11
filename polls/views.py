from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CategorySerializer

class Categories(APIView):
    def get(self, _):
        return Response('GET', status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            
        return Response({"status": True, "message": "Category created"}, status=status.HTTP_201_CREATED)
