from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('news/', PostsList.as_view()),
   path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),

]