from django.contrib import admin

# Register your models here.
from .models import Category, Post, Author

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)