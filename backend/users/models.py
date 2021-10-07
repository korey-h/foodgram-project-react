from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscribe(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='subscriptions')
    subscription = models.ForeignKey(User,
                                     on_delete=models.CASCADE,
                                     related_name='followers')

    class Meta:
        unique_together = ['user', 'subscription']


class Recipes(models.Model):
    pass


class Ingridients(models.Model):
    name = models.TextField(
        max_length=200, unique=True,
        error_messages={'unique': 'Такой ингридиент уже создан'},
        verbose_name='Название ингридиента')
    measurement_unit = models.TextField(
        max_length=200, verbose_name='единица измерения')


class IngridientAmount(models.Model):
    name = models.ForeignKey(
        Ingridients,
        on_delete=models.CASCADE,
        related_name='recipes')

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingridients')

    amount = models.IntegerField(
        default=0,
        help_text='Если количество выбирается по вкусу, впишите здесь ноль')
