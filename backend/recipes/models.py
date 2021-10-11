from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredients(models.Model):
    name = models.TextField(
        max_length=200, unique=True,
        error_messages={'unique': 'Такой ингридиент уже создан'},
        verbose_name='Название ингридиента')

    measurement_unit = models.TextField(
        max_length=200, verbose_name='единица измерения')


class Recipes(models.Model):

    tags = models.ManyToManyField(
        'Tags',
        related_name='tags')

    image = models.ImageField(upload_to='media/')

    name = models.TextField(
        max_length=200, unique=True,
        verbose_name='Название блюда')

    text = models.TextField(verbose_name='Описание рецепта')

    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[MinValueValidator(
            1, message='Время должно быть больше 1 минуты')
        ])


class IngredientAmount(models.Model):
    name = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='amount'
        )

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredients')

    amount = models.IntegerField(
        default=1,
        help_text='Если количество выбирается по вкусу, впишите здесь ноль')

    class Meta:
        unique_together = ['recipe', 'name']


class Tags(models.Model):
    name = models.TextField(
        max_length=200, verbose_name='Название тега')

    color = models.CharField(max_length=7, null=True, blank=True)

    slug = models.SlugField(max_length=200, null=True, blank=True)


class Favorites(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipes,
                               on_delete=models.CASCADE,
                               related_name='users')

    class Meta:
        unique_together = ['user', 'recipe']
