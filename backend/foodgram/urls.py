"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from recipes import views as recipes_views
from rest_framework.routers import SimpleRouter
from users import views as user_views

router_users = SimpleRouter()
router_recipes = SimpleRouter()
router_users.register("users",
                      user_views.CustomUserViewSet)
router_users.register("users",
                      user_views.SubscribeViewSet)

router_recipes.register("ingredients",
                        recipes_views.IngredientsViewSet)
router_recipes.register("recipes",
                        recipes_views.RecipesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/subscriptions/',
         user_views.SubscribeViewSet.as_view({'get': 'list'})),
    path('api/', include(router_users.urls)),
    path('api/', include(router_recipes.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
]
