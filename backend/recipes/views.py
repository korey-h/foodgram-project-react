import csv

from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, permissions 
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .filters import RecipesFilter
from .models import Favorites, Ingredients, IngredientAmount
from .models import Recipes, ShoppingCart, Tags
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    FavoritesSerializer,
    IngredientsSerializer,
    RecipesSerializer,
    ShoppingCartSerializer,
    TagsSerializer)


class IngredientsViewSet(ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    http_method_names = ['get', ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]


class RecipesViewSet(ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    filterset_class = RecipesFilter
    filter_backends = (DjangoFilterBackend,)
    pagination_class = pagination.PageNumberPagination

    @action(["get", "delete"], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        request.data.update({'id': kwargs['pk'], })
        self.queryset = Favorites.objects.filter(user=request.user.id)
        self.serializer_class = FavoritesSerializer
        self.lookup_url_kwarg = 'pk'
        self.lookup_field = 'recipe'
        if request.method == "GET":
            return self.create(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    @action(["get", "delete"], detail=True,
            permission_classes=[permissions.IsAuthenticated],
            filter_backends=[])
    def shopping_cart(self, request, *args, **kwargs):
        request.data.update({'id': kwargs['pk'], })
        self.queryset = ShoppingCart.objects.filter(user=request.user.id)
        self.serializer_class = ShoppingCartSerializer
        self.lookup_url_kwarg = 'pk'
        self.lookup_field = 'recipe'
        if request.method == "GET":
            return self.create(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    @action(["get"], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request, *args, **kwargs):
        recipes = ShoppingCart.objects.filter(
                    user=request.user.id).values_list('recipe', flat=True)
        queryset = IngredientAmount.objects.select_related().filter(
                    recipe__in=recipes)
        sum_queryset = queryset.values('name__name', 'name__measurement_unit'
                                       ).annotate(Sum('amount'))
        cvv_data = sum_queryset.values_list(
                    'name__name', 'amount__sum', 'name__measurement_unit')

        response = HttpResponse(content_type='text/csv; charset="UTF-8"')
        response['Content-Disposition'] = 'attachment; filename="Shopping_cart.csv"'  # noqa
        writer = csv.writer(response)
        writer.writerow(['Ингридиенты', 'Количество', 'ед. изм.'])
        writer.writerows(cvv_data)
        return response


class TagsViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    http_method_names = ['get', ]
    permission_classes = []
