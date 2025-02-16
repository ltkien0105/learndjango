from django.urls import path

from .views import UserPosts, UserComments

urlpatterns = [
    path("<int:user_id>/posts/", UserPosts.as_view(), name="user-get-posts"),
    path("<int:user_id>/comments/", UserComments.as_view(), name="user-get-comments"),
]