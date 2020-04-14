import re
from collections import namedtuple
from typing import Dict, Optional

import pytest

from src.common_log_format import regex

TestCase = namedtuple('TestCase', 'given_expression given_string expected_result')


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # LOG_AUTHUSER
        TestCase(regex.Atom.LOG_AUTHUSER, '-', {'authuser': '-'}),
        TestCase(regex.Atom.LOG_AUTHUSER, 'bar', {'authuser': 'bar'}),
        # LOG_CONTENT_SIZE
        TestCase(regex.Atom.LOG_CONTENT_SIZE, '0', {'content_size': '0'}),
        TestCase(regex.Atom.LOG_CONTENT_SIZE, '58973459', {'content_size': '58973459'}),
        # Atom.LOG_DATE
        TestCase(regex.Atom.LOG_DATE, '10/Oct/2000', {'year': '2000', 'month': 'Oct', 'day': '10'}),
        TestCase(regex.Atom.LOG_DATE, '10/Oct/98', None),
        # LOG_HTTP_STATUS
        TestCase(regex.Atom.LOG_HTTP_STATUS, '101', {'http_status': '101'}),
        TestCase(regex.Atom.LOG_HTTP_STATUS, '202', {'http_status': '202'}),
        TestCase(regex.Atom.LOG_HTTP_STATUS, '303', {'http_status': '303'}),
        TestCase(regex.Atom.LOG_HTTP_STATUS, '505', {'http_status': '505'}),
        TestCase(regex.Atom.LOG_HTTP_STATUS, '99', None),
        TestCase(regex.Atom.LOG_HTTP_STATUS, '700', None),
        # LOG_REFERER
        TestCase(regex.Atom.LOG_REFERER, '"http://www.example.com/start.html"', {'referer': 'http://www.example.com/start.html'}),
        TestCase(regex.Atom.LOG_REFERER, '"ftps://www.example.com/file.php"', {'referer': 'ftps://www.example.com/file.php'}),
        TestCase(regex.Atom.LOG_REFERER, '"www.example.com"', None),
        # LOG_RFC931
        TestCase(regex.Atom.LOG_RFC931, '-', {'user_identifier': '-'}),
        TestCase(regex.Atom.LOG_RFC931, 'foo', {'user_identifier': 'foo'}),
        # LOG_USER_AGENT
        TestCase(regex.Atom.LOG_USER_AGENT, '"Mozilla/4.08 [en] (Win98; I ;Nav)"', {'user_agent': 'Mozilla/4.08 [en] (Win98; I ;Nav)'}),
        TestCase(regex.Atom.LOG_USER_AGENT, '"Foo Bar"', {'user_agent': 'Foo Bar'}),
    )
)
def test_atom(
    given_expression: str,
    given_string: str,
    expected_result: Optional[Dict[str, str]],
) -> None:
    result = re.match(rf'^{given_expression}$', given_string)

    if expected_result is None:
        assert result is None, f'Expected no match, but got: {repr(result.groupdict())}'
    else:
        assert result is not None, f'Expected match, but got: None'
        assert result.groupdict() == expected_result


COMMON_LOG_FORMAT_1 = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326'
COMMON_LOG_FORMAT_2 = '127.0.0.1 - - [19/Jan/2005:21:47:11 +0000] "GET /brum.css HTTP/1.1" 304 0'

COMBINED_LOG_FORMAT_1 = '127.0.0.1 - frank [10/Oct/2000:13:55:36 +0130] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/start.html" "Mozilla/4.08 [en] (Win98; I ;Nav)"'


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # Common Log Format
        TestCase(
            regex.HTTPD,
            COMMON_LOG_FORMAT_1,
            {
                'ip': '127.0.0.1',
                'user_identifier': '-',
                'authuser': 'frank',
                'year': '2000', 'month': 'Oct', 'day': '10',
                'hour': '13', 'minute': '55', 'second': '36', 'microsecond': None,
                'timezone': '-0700',
                'message': 'GET /apache_pb.gif HTTP/1.0',
                'http_status': '200',
                'content_size': '2326',
                'referer': None,
                'user_agent': None,
            },
        ),
        TestCase(
            regex.HTTPD,
            COMMON_LOG_FORMAT_2,
            {
                'ip': '127.0.0.1',
                'user_identifier': '-',
                'authuser': '-',
                'year': '2005', 'month': 'Jan', 'day': '19',
                'hour': '21', 'minute': '47', 'second': '11', 'microsecond': None,
                'timezone': '+0000',
                'message': 'GET /brum.css HTTP/1.1',
                'http_status': '304',
                'content_size': '0',
                'referer': None,
                'user_agent': None,
            },
        ),
        # Combined Log Format
        TestCase(
            regex.HTTPD,
            COMBINED_LOG_FORMAT_1,
            {
                'ip': '127.0.0.1',
                'user_identifier': '-',
                'authuser': 'frank',
                'year': '2000', 'month': 'Oct', 'day': '10',
                'hour': '13', 'minute': '55', 'second': '36', 'microsecond': None,
                'timezone': '+0130',
                'message': 'GET /apache_pb.gif HTTP/1.0',
                'http_status': '200',
                'content_size': '2326',
                'referer': 'http://www.example.com/start.html',
                'user_agent': 'Mozilla/4.08 [en] (Win98; I ;Nav)',
            },
        ),
    ),
)
def test_molecule_httpd(
    given_expression: re.Pattern,
    given_string: str,
    expected_result: Optional[Dict[str, str]],
) -> None:
    result = given_expression.match(given_string)

    if expected_result is None:
        assert result is None, f'Expected no match, but got: {repr(result.groupdict())}'
    else:
        assert result is not None, f'Expected match, but got: None'
        assert result.groupdict() == expected_result
