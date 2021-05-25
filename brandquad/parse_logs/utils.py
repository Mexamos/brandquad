import re
from datetime import datetime
import logging
import typing

from requests import Session
from requests.models import Response

from parse_logs.type_aliases import ParsedLog

logger = logging.getLogger('utils')

PARSE_REGEX = '([\d\.]+).+?\[(.+)?\] \"(\w+) (.+?)\s.+?\s(\d+)\s(.+?)\s'


class RequestError(Exception):
    def __init__(self, status: int):
        self.message = f'Request error: {status}'
        super().__init__(self.message)


class InvalidLog(Exception):
    def __init__(self, log: str):
        self.message = f'Invalid log: {log}'
        super().__init__(self.message)


def make_request(
    url: str, method: str = 'GET', session: Session = Session()
) -> Response:
    response = session.request(method, url)

    if response.ok is False:
        raise RequestError(response.status_code)
    return response


def parse_log(log: str) -> typing.Optional[ParsedLog]:
    match = re.search(PARSE_REGEX, log)
    if match is None:
        raise InvalidLog(log)

    try:
        date = datetime.strptime(match.group(2), '%d/%b/%Y:%H:%M:%S %z')
        size = match.group(6)
        response_size = int(size) if size.isdigit() else None

        parsed_log = {
            'ip': match.group(1),
            'date': date,
            'method': match.group(3),
            'uri': match.group(4),
            'response_status': int(match.group(5)),
            'response_size': response_size,
        }
    except ValueError:
        raise InvalidLog(log)

    return parsed_log
