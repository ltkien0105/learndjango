from django.urls import path

from .views import Categories, Threads, Posts

urlpatterns = [
    path("categories/", Categories.as_view(), name="category-list"),
    path("categories/<int:id>", Categories.as_view(), name="category"),
    path("threads/", Threads.as_view(), name="thread-list"),
    path("threads/add/", Threads.as_view(), name="thread"),
    path("threads/<int:id>", Threads.as_view(), name="thread"),
    path("posts/", Posts.as_view(), name="post-list"),
    path("posts/<int:id>", Posts.as_view(), name="posts"),
    # path("posts/", views.index, name="posts"),
]