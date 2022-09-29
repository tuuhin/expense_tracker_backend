from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def number_lt_zero(number):
    if number < 0:
        raise ValidationError(
            gettext_lazy(f'{number} is is not greater than zero'),
        )
