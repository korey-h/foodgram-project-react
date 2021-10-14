from django.contrib import admin

from .models import (
    Favorites,
    Ingredients,
    IngredientAmount,
    Recipes,
    Tags,
    ShoppingCart)


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    empty_value_display = '-пусто-'


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('name', 'recipe', 'amount', 'unit')
    search_fields = ('name', 'recipe')
    list_filter = ('recipe', )
    empty_value_display = '-пусто-'

    def unit(self, obj):
        return Ingredients.objects.get(name=obj.name).measurement_unit


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'cooking_time', 'user')
    search_fields = ('name', 'text', )
    list_filter = ('user', 'tags')
    empty_value_display = '-пусто-'


class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('color',)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
