from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.FloatField(default=0.0)

class Category(models.Model):
    category_name = models.CharField(max_length=65, unique=True)

class Post(models.Model):
    #Запретить удаление постов при удалении автора выглядит логичным, даже если корреспондент уволился, новость или статья остается
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    article = 'AR'
    news_post = 'NP'

    POST_TYPES = [
        (article, 'Статья'),
        (news_post, 'Новость')
    ]

    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=news_post)
    post_created = models.DateTimeField(auto_now_add=True)
    category_names = models.ManyToManyField(Category, through = 'PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.DecimalField(default=0)

class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.DecimalField(default=0)



