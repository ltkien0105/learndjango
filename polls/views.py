from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from .serializers import CategorySerializer

class Categories(APIView):
    serializer = CategorySerializer
    
    def get(self, request):
        return Response('GET', status=status.HTTP_200_OK)
    
    def post(self, _):
        return HttpResponse("POST")
