from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Favorites, IngredientAmount, Ingredients, Recipes, Tags

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


class FavoritesSerializer(serializers.ModelSerializer):
    id = SlugRelatedField(queryset=Recipes.objects.all(),
                          slug_field='id', source='recipe')

    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True)

    class Meta:
        model = Favorites
        fields = ['id', 'name', 'image', 'cooking_time']

    def create(self, validated_data):
        obj = Favorites.objects.get_or_create(
            user=self.context['request'].user,
            recipe=validated_data['recipe'])
        return obj[0]


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientsAmountSerializer(many=True, )
    tags = SlugRelatedField(queryset=Tags.objects.all(),
                            slug_field='id', many=True)

    class Meta:
        model = Recipes
        fields = ['id', 'name', 'cooking_time', 'ingredients',
                  'tags', 'image', 'text']
        extra_kwargs = {'image': {'required': False}, }

    def to_representation(self, instance):
        self.fields['tags'] = TagsSerializer(many=True, )
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        # print('>>>Recipes update validated_data>>>', validated_data)
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
            if amount > 0:
                obj.amount = amount
                obj.save()
            else:
                obj.delete()

        return instance

    def create(self, validated_data):
        # print('>>>Recipes update validated_data>>>', validated_data)
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        for ingredient in ingredients_data:
            IngredientAmount.objects.create(recipe=recipe, **ingredient)
        recipe.tags.set(tags_data)
        recipe.save()

        return recipe
