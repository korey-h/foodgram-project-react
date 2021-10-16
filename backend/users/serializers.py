from django.contrib.auth import get_user_model
from djoser.conf import default_settings
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from .models import Subscribe
from recipes.models import Recipes

User = get_user_model()
default_settings["SERIALIZERS"]["user_create"] = 'users.serializers.CustomUserCreateSerializer' # noqa
default_settings["SERIALIZERS"]["user"] = 'users.serializers.CustomUserSerializer' # noqa
default_settings["SERIALIZERS"]["current_user"] = 'users.serializers.CustomUserSerializer' # noqa


class CustomUserSerializer(UserSerializer):
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribe']

    def get_is_subscribe(self, obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return False
        author = obj
        return Subscribe.objects.filter(
            user=current_user.id, subscription=author.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password', 'id')
        extra_kwargs = {'email': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True}, }


class SimpleRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipes
        fields = ['id', 'name', 'image', 'cooking_time', ]


class InfoSubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribe', 'recipes_count', 'recipes']

    def get_recipes_count(self, obj):
        return obj.user_recipes.count()

    def get_recipes(self, obj):
        obj = obj.user_recipes.all()
        try:
            params = self.context['request'].query_params
            limit = int(params['recipes_limit'])
            obj = obj[:limit]

        except (KeyError, ValueError):
            pass

        finally:
            return SimpleRecipeSerializer(obj, many=True).data


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = '__all__'

    def validate(self, attrs):
        author = attrs.get('subscription')
        user = self.context.get('request').user
        if user == author:
            raise ParseError(detail='Нельзя подписаться на самого себя.')
        return attrs

    def to_representation(self, obj):
        return InfoSubscribeSerializer(
            obj.subscription, context=self.context).data
