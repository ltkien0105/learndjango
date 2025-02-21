from django.db import models
from django.conf import settings

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.category_name
    
class Post(models.Model):
    title = models.CharField(max_length=200, default='')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
