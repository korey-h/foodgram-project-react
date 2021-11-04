import re

from django.core.exceptions import ValidationError


def color_validator(value):
    if not re.fullmatch(r'#([0-9A-Fa-f]{3}){1,2}', value):
        raise ValidationError(
            f'{value} - неправильный формат цветового кода'
        )
