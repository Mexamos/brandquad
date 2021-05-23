import logging

from django.core.management.base import BaseCommand

from parse_logs import validators
from parse_logs.views import process_save_logs
from parse_logs import utils

logger = logging.getLogger('manage-commands')


class Command(BaseCommand):
    help = 'Parse and save logs from URL'

    def handle(self, *args, **options):
        url = options['url'][0]
        rows_number = options['rows_number'][0] if len(options['rows_number']) > 0 else None

        try:
            validators.validate_url(url)

            process_save_logs(url, rows_number=rows_number)
        except (
            validators.InvalidURL,
            utils.RequestError,
        ) as error:
            logger.error(error.message)

        logger.info('Logs successfully saved')

    def add_arguments(self, parser):
        parser.add_argument(
            'url',
            type=str,
            nargs=1,
            help='URL for get logs',
        )

        parser.add_argument(
            'rows_number',
            type=int,
            nargs='*',
            help='Number of log rows',
        )
