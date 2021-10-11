from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import pagination, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .models import Subscribe
from .serializers import CustomUserSerializer, SubscribeSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.all()


class SubscribeViewSet(ModelViewSet):
    http_method_names = ['get', 'delete', ]
    serializer_class = SubscribeSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = pagination.PageNumberPagination
    queryset = Subscribe.objects.all()
    lookup_url_kwarg = 'id'
    lookup_field = 'subscription'

    def create(self, request, *args, **kwargs):
        subscription = get_object_or_404(User, id=self.kwargs['id'])
        user = request.user.id
        data = {'subscription': subscription.id,
                'user': user}
        request.data.update(data)
        return super().create(request, *args, **kwargs)

    @action(["get", "delete"], detail=True)
    def subscribe(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.create(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)
