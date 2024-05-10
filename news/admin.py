from django.contrib import admin

# Register your models here.
from .models import Category, Post, Author, PostCategory

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(PostCategory)