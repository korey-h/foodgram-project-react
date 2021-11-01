import re

from django.core.exceptions import ValidationError


def color_validator(value):
    if not re.match(r'#[0-9A-Fa-f]{6}', value):
        raise ValidationError(
            f'{value} - неправильный формат цветового кода'
        )


def negative_validator(value):
    if value < 0:
        raise ValidationError(
            'Количество не может быть отрицательным'
        )
