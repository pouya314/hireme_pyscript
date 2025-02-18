from decimal import Decimal

from .errors import ValidationError


def required(provided_answer):
    if not provided_answer:
        raise ValidationError('This field is required.')


def is_string(provided_answer):
    try:
        str(provided_answer)
    except Exception as e:
        raise ValidationError('This field must be a string.')


def is_decimal(provided_answer):
    try:
        Decimal(provided_answer)
    except Exception as e:
        raise ValidationError('This field must be a decimal number.')
