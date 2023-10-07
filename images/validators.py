from django.core.exceptions import ValidationError


def validate_expiration_time(value):
    """
    Validates if input value for expiration time is
    between MIN_TIME and MAX_TIME values.
    """
    MIN_TIME = 300
    MAX_TIME = 30000
    if value is not None and not MIN_TIME <= value <= MAX_TIME:
        raise ValidationError("Value must be a number between 300 and 30000")
