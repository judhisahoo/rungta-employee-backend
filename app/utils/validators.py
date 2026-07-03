from datetime import datetime

from .exceptions import ValidationError


EMPTY_VALUES = (None, "", "string", "null", "None")


def normalize_blank(value):
    if isinstance(value, str):
        value = value.strip()
    return value


def is_blank(value):
    return normalize_blank(value) in EMPTY_VALUES


def parse_date(value, field_name):
    value = normalize_blank(value)
    if value in EMPTY_VALUES:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("{} must be in YYYY-MM-DD format".format(field_name))


def validate_choice(value, valid_values, field_name):
    value = normalize_blank(value)
    if value in EMPTY_VALUES:
        return value
    if value not in valid_values:
        raise ValidationError(
            "{} must be one of: {}".format(field_name, ", ".join(sorted(valid_values)))
        )
    return value

