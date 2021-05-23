import re
from datetime import datetime
import logging
import typing

from requests import Session
from requests.models import Response

logger = logging.getLogger('utils')

PARSE_REGEX = '([\d\.]+).+?\[(.+)?\] \"(\w+) (.+?)\s.+?\s(\d+)\s(.+?)\s'


class RequestError(Exception):
    def __init__(self, status: int):
        self.message = f'Request error: {status}'
        super().__init__(self.message)


def make_request(
    url: str, method: str = 'GET', session: Session = Session()
) -> Response:
    response = session.request(method, url)

    if response.ok is False:
        raise RequestError(response.status_code)
    return response


def parse_logs(
    url: str, rows_number: int = None
) -> typing.List[typing.Optional[typing.Dict[str, typing.Union[str, datetime, int]]]]:
    response = make_request(url)

    logs = []
    lines = response.text.split('\n')
    if rows_number is not None:
        lines = lines[:rows_number + 1]

    for line in lines:
        match = re.search(PARSE_REGEX, line)
        if match is None:
            logger.warn(f'Invalid log line: {line}')
            continue

        try:
            date = datetime.strptime(match.group(2), '%d/%b/%Y:%H:%M:%S %z')
            size = match.group(6)
            response_size = int(size) if size.isdigit() else None

            logs.append(
                {
                    'ip': match.group(1),
                    'date': date,
                    'method': match.group(3),
                    'uri': match.group(4),
                    'response_status': int(match.group(5)),
                    'response_size': response_size,
                }
            )
        except ValueError:
            logger.warn(f'Invalid log date: {line}')
            continue

    return logs
