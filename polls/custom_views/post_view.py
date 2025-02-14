from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from ..serializers import PostSerializer
from ..models import Post
from auth.authentication import CookieJWTAuthentication

class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        thread_id = self.request.query_params.get('thread')
        if thread_id:
            return Post.objects.filter(thread_id=thread_id)

        return Post.objects.all()

    def post(self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)
    
class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
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
    
    
    
