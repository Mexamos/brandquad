from datetime import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.management import call_command

from parse_logs.models import DataLog

LOG = {
    'ip': '255.255.255.255',
    'method': 'GET',
    'uri': '/test',
    'response_status': 200,
    'response_size': 123,
}


class DataLogModelTests(TestCase):
    def test_create_datalog(self):
        date = timezone.now()
        LOG['date'] = date
        data_log = DataLog(**LOG)
        data_log.save()

        self.assertIsNotNone(data_log.id)

    def test_create_datalog_error(self):
        date = datetime.now()
        LOG['date'] = date
        data_log = DataLog(**LOG)

        with self.assertWarns(RuntimeWarning):
            data_log.save()


class ParseLogsCommandTest(TestCase):
    def test_parse_logs_command(self):
        logs_number = 10
        call_command('parse_logs', ['http://www.almhuette-raith.at/apache-log/access.log'], [logs_number])

        data_logs = DataLog.objects.all()
        self.assertIs(len(data_logs), logs_number)
