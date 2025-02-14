from django.urls import path

from .views import *

urlpatterns = [
    # Categories
    path("categories/", category_view.CategoryListCreateView.as_view(), name="category-list-add"),
    path("categories/<int:pk>", category_view.CategoryRetrieveUpdateDestroyView.as_view(), name="category-get-update-delete"),
    # Threads
    path("threads/", thread_view.ThreadListCreateView.as_view(), name="thread-list-add"),
    path("threads/<int:pk>", thread_view.ThreadRetrieveUpdateDestroyView.as_view(), name="thread-get-update-delete"),
    # Posts
    path("posts/", post_view.PostListCreateView.as_view(), name="post-list"),
    path("posts/<int:pk>", post_view.PostRetrieveUpdateDestroyView.as_view(), name="post-get-update-delete"),
]