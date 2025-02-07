from django.urls import path

from .views import Categories

urlpatterns = [
    path("categories/", Categories.as_view(), name="categories"),
    # path("threads/", views.index, name="threads"),
    # path("posts/", views.index, name="posts"),
]