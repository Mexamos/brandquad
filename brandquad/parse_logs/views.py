import logging

from django.db import transaction

from parse_logs import utils
from parse_logs.models import DataLog

logger = logging.getLogger('views')

BATCH_SIZE = 100000


@transaction.atomic
def process_save_logs(url: str, rows_number: int = None) -> None:
    response = utils.make_request(url)

    logs = []
    for index, chunk in enumerate(
        response.iter_lines(chunk_size=1024, decode_unicode=True)
    ):
        if rows_number is not None and index > rows_number:
            break

        try:
            log = utils.parse_log(chunk)
        except utils.InvalidLog as error:
            logger.warn(error.message)
        else:
            logs.append(DataLog(**log))

    DataLog.objects.bulk_create(logs, BATCH_SIZE)
