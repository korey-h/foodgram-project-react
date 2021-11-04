from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views as user_views

router_users = SimpleRouter()

router_users.register("users",
                      user_views.CustomUserViewSet)
router_users.register("users",
                      user_views.SubscribeViewSet)


urlpatterns = [
    path('users/subscriptions/',
         user_views.SubscribeViewSet.as_view({'get': 'list'})),
    path('', include(router_users.urls)),
]
