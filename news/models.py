from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.contrib.auth.models import User

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.author.username
    
    def update_rating(self):
        # Суммарный рейтинг каждой статьи автора умножается на 3
        posts_rate = self.post_set.aggregate(total_rate=Sum('post_rating'))['total_rate'] or 0
        posts_rate *= 3
       
        # Суммарный рейтинг всех комментариев автора
        comments_rate = self.author.comment_set.aggregate(total_rating=Sum('comment_rating'))['total_rating'] or 0

        # Суммарный рейтинг всех комментариев к статьям автора
        post_comments_rate = Comment.objects.filter(related_post__author=self).aggregate(total_rating=Sum('comment_rating'))['total_rating'] or 0

        # Обновление рейтинга автора
        self.user_rating = posts_rate + comments_rate + post_comments_rate
        self.save()

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    category_name = models.CharField(max_length=65, unique=True)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Post(models.Model):
    #Запретить удаление постов при удалении автора выглядит логичным, даже если корреспондент уволился, новость или статья остается
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    article = 'AR'
    news_post = 'NP'

    #Список выбора
    POST_TYPES = [
        (article, 'Статья'),
        (news_post, 'Новость')
    ]

    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=news_post)
    post_created = models.DateTimeField(auto_now_add=True)
    category_names = models.ManyToManyField(Category, through = 'PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    #Методы
    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    #Превью поста
    def prewiew(self):
        if len(self.post_text) > 124:
            prew_text = self.post_text[:124] + '...'
            return prew_text
        else:
            return self.post_text
        
    def __str__(self):
        return f'{self.post_title}'
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

#Модель для связи "Многие к многим"
class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    #Методы
    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

        
class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )

    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
