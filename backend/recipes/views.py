import csv

from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, permissions 
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .filters import RecipesFilter
from .models import Ingredients, IngredientAmount, Recipes, Tags
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

    def get_queryset(self):
        if self.action == 'shopping_cart':
            return self.request.user.shopping_cart.all()
        elif self.action == 'favorite':
            return self.request.user.favorites.all()
        else:
            return super().get_queryset()

    def get_object(self):
        if self.action == 'shopping_cart' or self.action == 'favorite':           
            filter_kwargs = {'recipe': self.kwargs['pk']}
            return get_object_or_404(self.get_queryset(), **filter_kwargs)
        else:
            return super().get_object()

    def get_serializer_class(self):
        if self.action == 'shopping_cart':
            return ShoppingCartSerializer
        elif self.action == 'favorite':
            return FavoritesSerializer  
        else:
            return super().get_serializer_class()

    @action(['get', 'delete'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        request.data.update({'id': kwargs['pk'], })
        if request.method == 'GET':
            return self.create(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return self.destroy(request, *args, **kwargs)

    @action(["get", "delete"], detail=True,
            permission_classes=[permissions.IsAuthenticated],)
    def shopping_cart(self, request, *args, **kwargs):
        request.data.update({'id': kwargs['pk'], })
        if request.method == "GET":
            return self.create(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    @action(["get"], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request, *args, **kwargs):
        recipes = request.user.shopping_cart.values_list('recipe', flat=True)
        queryset = IngredientAmount.objects.select_related().filter(
                    recipe__in=recipes)
        sum_queryset = queryset.values('name__name', 'name__measurement_unit'
                                       ).annotate(Sum('amount'))
        cvv_data = sum_queryset.values_list(
                    'name__name', 'amount__sum', 'name__measurement_unit')

        response = HttpResponse(content_type='text/csv; charset="UTF-8"')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="Shopping_cart.csv"')
        writer = csv.writer(response)
        writer.writerow(['Ингридиенты', 'Количество', 'ед. изм.'])
        writer.writerows(cvv_data)
        return response


class TagsViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    http_method_names = ['get', ]
    permission_classes = []
