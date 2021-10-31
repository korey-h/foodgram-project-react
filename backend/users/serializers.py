from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes import serializers as rec_serializers
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from .models import Subscribe

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribe']

    def get_is_subscribe(self, obj):
        current_user = self.context['request'].user
        return (not current_user.is_anonymous and Subscribe.objects.filter(
                user=current_user, subscription=obj).exists()
                )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password', 'id')
        extra_kwargs = {'email': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True}, }


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
            return rec_serializers.SimpleRecipeSerializer(obj, many=True).data


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
