from parse_logs.utils import parse_logs
from parse_logs.models import DataLog


def process_save_logs(url: str) -> None:
    logs = parse_logs(url)

    # for log in logs:
    #     DataLog(**log).save()
