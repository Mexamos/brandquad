from parse_logs.utils import parse_logs
from parse_logs.models import DataLog


def process_save_logs(url: str, rows_number: int = None) -> None:
    logs = parse_logs(url, rows_number=rows_number)

    for log in logs:
        DataLog(**log).save()
