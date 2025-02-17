from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from ..serializers import PostSerializer
from ..models import Post
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return Post.objects.filter(category_id=category_id)

        return Post.objects.all()
    
    def post(self, request, *args, **kwargs):
        self.authentication_classes = [SessionAuthentication]
        self.permission_classes = [IsAuthenticated]
        return super().post(request, *args, **kwargs)
    
class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    
    def update(self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)
    
