from django.urls import path

from .views import UserPosts, UserComments, UserUpdateProfile, UserUpdateAvatar

urlpatterns = [
    path("<int:user_id>/posts/", UserPosts.as_view(), name="user-get-posts"),
    path("<int:user_id>/comments/", UserComments.as_view(), name="user-get-comments"),
    path("<int:pk>/avatar", UserUpdateAvatar.as_view(), name="user-update-avatar"),
    path("<int:pk>", UserUpdateProfile.as_view(), name="user-update-profile"),
]