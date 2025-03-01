from django.urls import path

from .views import *

urlpatterns = [
    # Categories
    path("categories/", category_view.CategoryListCreateView.as_view(), name="category-list-add"),
    path("categories/<int:pk>", category_view.CategoryRetrieveUpdateDestroyView.as_view(), name="category-get-update-delete"),
    # Posts
    path("posts/", post_view.PostListCreateView.as_view(), name="post-list-add"),
    path("posts/search/", post_view.PostSearch.as_view(), name="post-search"),
    path("posts/<int:pk>/like", post_view.PostUpdateLikeCount.as_view(), name="post-update-like"),
    path("posts/<int:pk>/comments", post_view.PostGetComments.as_view(), name="post-get-comments"),
    path("posts/<int:pk>", post_view.PostRetrieveUpdateDestroyView.as_view(), name="post-get-update-delete"),
    # Comments
    path("comments/", comment_view.CommentListCreateView.as_view(), name="comment-list"),
    path("comments/<int:pk>", comment_view.CommentRetrieveUpdateDestroyView.as_view(), name="comment-get-update-delete"),
]