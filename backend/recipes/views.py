from rest_framework import filters, permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .models import Favorites, Ingredients, Recipes
from .serializers import (FavoritesSerializer, IngredientsSerializer,
                          RecipesSerializer)


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

    @action(["get", "delete"], detail=True)
    def favorite(self, request, *args, **kwargs):
        request.data.update({'id': kwargs['pk'], })
        self.queryset = Favorites.objects.filter(user=request.user.id)
        self.serializer_class = FavoritesSerializer
        self.permission_classes = (permissions.IsAuthenticated,)
        self.lookup_url_kwarg = 'pk'
        self.lookup_field = 'recipe'
        if request.method == "GET":
            return self.create(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)
