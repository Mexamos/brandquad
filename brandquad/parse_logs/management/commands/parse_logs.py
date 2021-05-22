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
        try:
            validators.validate_url(url)

            process_save_logs(url)
        except (
            validators.InvalidURL, utils.RequestError
        ) as error:
            logger.error(error.message)

    def add_arguments(self, parser):
        parser.add_argument(
            'url',
            type=str,
            nargs=1,
            help='URL for get logs',
        )