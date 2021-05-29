import typing
from unittest.mock import MagicMock
from unittest.mock import patch

from django.db.utils import IntegrityError
from django.utils import timezone
from django.test import TestCase
from django.core.management import call_command

from parse_logs.models import DataLog
from parse_logs.management.commands.parse_logs import logger as command_logger
from parse_logs.views import logger as views_logger
from parse_logs import utils

LOG = {
    'ip': '255.255.255.255',
    'method': 'GET',
    'uri': '/test',
    'response_status': 200,
    'response_size': 123,
}

LOG_LINES = [
    '13.66.139.0 - - [19/Dec/2020:13:57:26 +0100] "GET /index.php?option=com_phocagallery&view=category&id=1:almhuette-raith&Itemid=53 HTTP/1.1" 200 32653 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" "-"',
    '157.48.153.185 - - [19/Dec/2020:14:08:06 +0100] "GET /apache-log/access.log HTTP/1.1" 200 233 "-" "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" "-"',
    '157.48.153.185 - - [19/Dec/2020:14:08:08 +0100] "GET /favicon.ico HTTP/1.1" 404 217 "http://www.almhuette-raith.at/apache-log/access.log" "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" "-"',
    '216.244.66.230 - - [19/Dec/2020:14:14:26 +0100] "GET /robots.txt HTTP/1.1" 200 304 "-" "Mozilla/5.0 (compatible; DotBot/1.1; http://www.opensiteexplorer.org/dotbot, help@moz.com)" "-"',
    '54.36.148.92 - - [19/Dec/2020:14:16:44 +0100] "GET /index.php?option=com_phocagallery&view=category&id=2%3Awinterfotos&Itemid=53 HTTP/1.1" 200 30662 "-" "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)" "-"',
    '92.101.35.224 - - [19/Dec/2020:14:29:21 +0100] "GET /administrator/index.php HTTP/1.1" 200 4263 "" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)" "-"',
]
INVALID_LOG_LINE = '42.236.10.114 - - 19/Dec/2020:15:23:11 +0100 "GET /templates/jp_hotel/css/menu.css HTTP/1.1" 200 1457 "http://www.almhuette-raith.at/" "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 baidu.sogo.uc.UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN" "-"'
INVALID_LOG_DATE_LINE = '42.236.10.117 - - [19/12/2020:15:23:13 +0100] "GET /images/stories/slideshow/almhuette_raith_05.jpg HTTP/1.1" 200 77796 "http://www.almhuette-raith.at/" "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 baidu.sogo.uc.UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN" "-"'


class DataLogModelTests(TestCase):
    @staticmethod
    def get_log():
        return LOG.copy()

    def test_create_datalog(self):
        LOG = self.get_log()
        LOG['date'] = timezone.now()
        data_log = DataLog(**LOG)
        data_log.save()

        self.assertIsNotNone(data_log.id)

    def test_create_datalog_with_nullable_size(self):
        LOG = self.get_log()
        LOG['date'] = timezone.now()
        LOG['response_size'] = None
        data_log = DataLog(**LOG)
        data_log.save()

        self.assertIsNotNone(data_log.id)

    def test_create_datalog_error(self):
        LOG = self.get_log()
        data_log = DataLog(**LOG)

        with self.assertRaises(IntegrityError):
            data_log.save()


class ParseLogsCommandTest(TestCase):
    @staticmethod
    def get_response_mock(logs_lines: typing.List[str]):
        response_mock = MagicMock()
        response_mock.iter_lines = MagicMock(return_value=logs_lines)

        return response_mock

    def test_parse_logs_command(self):
        command_logger.info = MagicMock()
        logs_number = 10

        call_command(
            'parse_logs', ['http://www.almhuette-raith.at/apache-log/access.log'], [logs_number]
        )

        data_logs = DataLog.objects.all()

        self.assertIs(len(data_logs), logs_number)
        command_logger.info.assert_called_once_with('Logs successfully saved')

    def test_invalid_url(self):
        command_logger.error = MagicMock()
        invalid_url = 'http:///www.invalid-url.com'

        call_command('parse_logs', [invalid_url])

        command_logger.error.assert_called_once_with(f'Invalid url: {invalid_url}')

    def test_request_error(self):
        command_logger.error = MagicMock()
        error_url = 'https://httpstat.us/404'

        call_command('parse_logs', [error_url])

        command_logger.error.assert_called_once_with('Request error: 404')

    def test_invalid_log_format(self):
        views_logger.warn = MagicMock()

        response_mock = self.get_response_mock(LOG_LINES + [INVALID_LOG_LINE])

        with patch.object(utils, 'make_request', return_value=response_mock):

            call_command('parse_logs', ['http://www.almhuette-raith.at/apache-log/access.log'])

            data_logs = DataLog.objects.all()

            self.assertIs(len(data_logs), len(LOG_LINES))
            views_logger.warn.assert_called_once_with(f'Invalid log: {INVALID_LOG_LINE}')

    def test_invalid_log_date_format(self):
        views_logger.warn = MagicMock()

        response_mock = self.get_response_mock(LOG_LINES + [INVALID_LOG_DATE_LINE])

        with patch.object(utils, 'make_request', return_value=response_mock):

            call_command('parse_logs', ['http://www.almhuette-raith.at/apache-log/access.log'])

            data_logs = DataLog.objects.all()

            self.assertIs(len(data_logs), len(LOG_LINES))
            views_logger.warn.assert_called_once_with(f'Invalid log: {INVALID_LOG_DATE_LINE}')
