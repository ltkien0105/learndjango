from django.urls import path

from .views import Categories, Threads

urlpatterns = [
    path("categories/", Categories.as_view(), name="categories"),
    path("categories/<int:id>", Categories.as_view(), name="categories"),
    path("threads/", Threads.as_view(), name="threads"),
    path("threads/<int:id>", Threads.as_view(), name="threads"),
    # path("posts/", views.index, name="posts"),
]