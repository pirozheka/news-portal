from django.urls import path
# Импортируем созданное нами представление
from .views import (
    PostsList, PostDetail, NewsSearch, NewsCreate, PostEdit, PostDelete, ArticlesCreate
    )


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('news/', PostsList.as_view(), name = 'news_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/search/', NewsSearch.as_view(), name = 'news_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/create/', ArticlesCreate.as_view(), name = 'articles_create'),
   path('articles/<int:pk>/edit/', PostEdit.as_view(), name = 'articles_edit'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]