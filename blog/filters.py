from django_filters import FilterSet
from .models import Article
import django_filters

class ArticleFilter(FilterSet):
    category__name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Article
        fields = ['category__name']