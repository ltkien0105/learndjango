from django.contrib import admin

from .models import Category, Post, Thread

# Register your models here.
admin.site.register([Category, Post, Thread])
