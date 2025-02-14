from django.db.models import Count

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from ..serializers import CategorySerializer
from ..models import Category
from auth.authentication import CookieJWTAuthentication

class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        is_get_thread_count = self.request.query_params.get('thread_count')
        if is_get_thread_count and is_get_thread_count == '1':
            return Category.objects.annotate(thread_count=Count('thread'))

        return Category.objects.all()
    
    def post(self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)
    
class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CookieJWTAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    def update(self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)
    
