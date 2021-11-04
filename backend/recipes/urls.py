from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views as recipes_views

router_recipes = SimpleRouter()

router_recipes.register("ingredients",
                        recipes_views.IngredientsViewSet)
router_recipes.register("recipes",
                        recipes_views.RecipesViewSet)
router_recipes.register("tags",
                        recipes_views.TagsViewSet)

urlpatterns = [
    path('', include(router_recipes.urls)),
]
