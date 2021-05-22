import logging

from django.core.management.base import BaseCommand

from parse_logs import validators

logger = logging.getLogger('manage-commands')


class Command(BaseCommand):
    help = 'Parse and save logs from URL'

    def handle(self, *args, **options):
        url = options['url'][0]
        try:
            validators.validate_url(url)
        except validators.InvalidURL as error:
            logger.error(error.message)

    def add_arguments(self, parser):
        parser.add_argument(
            'url',
            type=str,
            nargs=1,
            help='URL for get logs',
        )