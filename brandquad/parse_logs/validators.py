from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

url_validator = URLValidator()


class InvalidURL(Exception):
    def __init__(self, url: str):
        self.message = f'Invalid url: {url}'
        super().__init__(self.message)


def validate_url(url: str):
    try:
        url_validator(url)
    except ValidationError:
        raise InvalidURL(url)