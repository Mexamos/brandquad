from typing import Optional
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

url_validator = URLValidator()


class ValidatorError(Exception):
    pass


class InvalidURL(ValidatorError):
    def __init__(self, url: str):
        self.message = f'Invalid url: {url}'
        super().__init__(self.message)


def validate_url(url: str) -> None:
    try:
        url_validator(url)
    except ValidationError:
        raise InvalidURL(url)