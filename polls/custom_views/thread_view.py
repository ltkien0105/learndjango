from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from ..serializers import ThreadSerializer
from ..models import Thread
from auth.authentication import CookieJWTAuthentication

class ThreadListCreateView(ListCreateAPIView):
    serializer_class = ThreadSerializer
    
    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return Thread.objects.filter(category_id=category_id)

        return Thread.objects.all()
    
    def post(self, request, *args, **kwargs):
        print(request.user)
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)
    
class ThreadRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CookieJWTAuthentication]
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()
    
    def update(self, request, *args, **kwargs):
        print(request.user)
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)
    
