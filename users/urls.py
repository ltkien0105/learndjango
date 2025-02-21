from django.urls import path

from .views import UserPosts, UserComments, UserRetrieveUpdateProfile, UserUpdateAvatar, UserChangePassword

urlpatterns = [
    path("<int:user_id>/posts/", UserPosts.as_view(), name="user-get-posts"),
    path("<int:user_id>/comments/", UserComments.as_view(), name="user-get-comments"),
    path("<int:pk>/avatar", UserUpdateAvatar.as_view(), name="user-update-avatar"),
    path("<int:pk>/change-password", UserChangePassword.as_view(), name="user-change-password"),
    path("<int:pk>", UserRetrieveUpdateProfile.as_view(), name="user-update-profile"),
]