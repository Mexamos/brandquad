from requests import Session


class RequestError(Exception):
    def __init__(self, status: int):
        self.message = f'Request error: {status}'
        super().__init__(self.message)


def make_request(
    url: str, method: str = 'GET', session: Session = Session()
):
    response = session.request(method, url)

    if response.ok is False:
        raise RequestError(response.status_code)

    return response


def parse_logs(url: str):
    response = make_request(url)
