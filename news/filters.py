from django_filters import FilterSet
from .models import Post

class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'category_names__category_name': ['icontains'],
        }