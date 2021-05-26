from datetime import datetime
from unittest.mock import MagicMock

from django.utils import timezone
from django.test import TestCase
from django.core.management import call_command

from parse_logs.models import DataLog
from parse_logs.management.commands.parse_logs import logger

LOG = {
    'ip': '255.255.255.255',
    'method': 'GET',
    'uri': '/test',
    'response_status': 200,
    'response_size': 123,
}


class DataLogModelTests(TestCase):
    def test_create_datalog(self):
        LOG['date'] = timezone.now()
        data_log = DataLog(**LOG)
        data_log.save()

        self.assertIsNotNone(data_log.id)

    def test_create_datalog_with_nullable_size(self):
        LOG['date'] = timezone.now()
        LOG['response_size'] = None
        data_log = DataLog(**LOG)
        data_log.save()

        self.assertIsNotNone(data_log.id)

    def test_create_datalog_error(self):
        LOG['date'] = timezone.now()
        data_log = DataLog(**LOG)

        with self.assertWarns(RuntimeWarning):
            data_log.save()


class ParseLogsCommandTest(TestCase):
    def test_parse_logs_command(self):
        logger.info = MagicMock()
        logs_number = 10
        call_command('parse_logs', ['http://www.almhuette-raith.at/apache-log/access.log'], [logs_number])

        data_logs = DataLog.objects.all()
        self.assertIs(len(data_logs), logs_number)
        logger.info.assert_called_once_with('Logs successfully saved')

    def test_invalid_url(self):
        logger.error = MagicMock()
        invalid_url = 'http:///www.invalid-url.com'

        call_command('parse_logs', [invalid_url])

        logger.error.assert_called_once_with(f'Invalid url: {invalid_url}')

    def test_request_error(self):
        logger.error = MagicMock()
        error_url = 'https://httpstat.us/404'

        call_command('parse_logs', [error_url])

        logger.error.assert_called_once_with('Request error: 404')
