from parse_logs.utils import parse_logs


def process_save_logs(url: str) -> None:
    logs = parse_logs(url)