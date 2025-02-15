from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from ..serializers import CommentSerializer
from ..models import Comment

class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        if post_id:
            return Comment.objects.filter(post_id=post_id)

        return Comment.objects.all()

    def post(self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)
    
class CommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
    def update(self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return Response(status=HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)
    
    
    
