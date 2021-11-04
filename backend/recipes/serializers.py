from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from users.serializers import CustomUserSerializer

from .models import (
    Favorites,
    IngredientAmount,
    Ingredients,
    Recipes,
    Tags,
    ShoppingCart)

User = get_user_model()


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ['id', 'name', 'measurement_unit']
        extra_kwargs = {'name': {'read_only': True},
                        'measurement_unit': {'read_only': True},
                        'id': {'required': True}}


class IngredientsAmountSerializer(serializers.ModelSerializer):
    id = SlugRelatedField(queryset=Ingredients.objects.all(),
                          slug_field='id', source='name')
    name = serializers.CharField(source='name.name', read_only=True)
    measurement_unit = serializers.CharField(source='name.measurement_unit',
                                             read_only=True)

    class Meta:
        model = IngredientAmount
        fields = ['id', 'name', 'amount', 'measurement_unit']


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'


class SimpleRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipes
        fields = ['id', 'name', 'image', 'cooking_time', ]


class FavoritesSerializer(serializers.ModelSerializer):
    id = SlugRelatedField(queryset=Recipes.objects.all(),
                          slug_field='id', source='recipe')

    class Meta:
        model = Favorites
        fields = ['id']

    def to_representation(self, instance):
        self.fields['id'] = SimpleRecipeSerializer(source='recipe')
        out = super().to_representation(instance)
        return out['id']


class ShoppingCartSerializer(FavoritesSerializer):

    class Meta:
        model = ShoppingCart
        fields = ['id']


class RecipesSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(source='user')
    ingredients = IngredientsAmountSerializer(many=True, )
    tags = SlugRelatedField(queryset=Tags.objects.all(),
                            slug_field='id', many=True)

    image = Base64ImageField(use_url=True)

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = [
            'id',
            'name', 
            'cooking_time',
            'author', 
            'ingredients',
            'tags',
            'image',
            'text',
            'is_favorited',
            'is_in_shopping_cart',
        ]

    def get_is_favorited(self, obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return False
        return current_user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return False
        return current_user.shopping_cart.filter(recipe=obj).exists()

    def to_representation(self, instance):
        self.fields['tags'] = TagsSerializer(many=True, )
        return super().to_representation(instance)

    def to_internal_value(self, data):
        self.fields['author'] = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all(),
            source='user')
        user = self.context['request'].user
        data.update({'author': user})
        return super().to_internal_value(data)

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.tags.set(tags_data)
        for ingredient in ingredients_data:
            amount = ingredient['amount']
            obj = IngredientAmount.objects.get_or_create(
                recipe=instance,
                name=ingredient['name'])[0]
            if amount == 0:
                obj.delete()

            else:
                obj.amount = amount
                obj.save()

        return instance

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        for ingredient in ingredients_data:
            IngredientAmount.objects.create(recipe=recipe, **ingredient)
        recipe.tags.set(tags_data)
        recipe.user = self.context['request'].user
        recipe.save()

        return recipe
