from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .models import Ingredients, Recipes
from .serializers import IngredientsSerializer, RecipesSerializer


class IngredientsViewSet(ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    http_method_names = ['get', ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]


class RecipesViewSet(ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
