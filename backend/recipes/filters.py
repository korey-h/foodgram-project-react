from django_filters import filters
from django_filters.rest_framework.filterset import FilterSet

from .models import Recipes


class RecipesFilter(FilterSet):
    author = filters.CharFilter(field_name='user__id',
                                lookup_expr='exact')
    is_favorited = filters.NumberFilter(method='get_favorites')
    is_in_shopping_cart = filters.NumberFilter(method='get_user_cart')

    class Meta:
        model = Recipes
        fields = ['user', 'tags']

    def get_favorites(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            queryset = queryset.filter(
                id__in=user.favorites.values_list('recipe', flat=True))
        return queryset

    def get_user_cart(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            queryset = queryset.filter(
                id__in=user.shopping_cart.values_list('recipe', flat=True))
        return queryset