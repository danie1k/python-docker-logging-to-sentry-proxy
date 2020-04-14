import re
from collections import namedtuple
from typing import Dict, Optional

import pytest

from src.nginx import regex

TestCase = namedtuple('TestCase', 'given_expression given_string expected_result')


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # NGINX_ERROR_DATE
        TestCase(regex.Atom.NGINX_ERROR_DATE, '1970/01/01', {'year': '1970', 'month': '01', 'day': '01'}),
        TestCase(regex.Atom.NGINX_ERROR_DATE, '2000/02/03', {'year': '2000', 'month': '02', 'day': '03'}),
        TestCase(regex.Atom.NGINX_ERROR_DATE, '2000-02-03', None),
        # NGINX_CID
        TestCase(regex.Atom.NGINX_CID, '0', {'connection_counter': '0'}),
        TestCase(regex.Atom.NGINX_CID, '345', {'connection_counter': '345'}),
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


NGINX_ERROR_1 = '2020/03/21 23:30:24 [crit] 30016#0: *4 stat() "/var/www/html/index.php" failed (13: Permission denied), client: 127.0.0.1, server: example.com, request: "GET /index.php HTTP/1.1", host: "example.com"'


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        TestCase(
            regex.NGINX_ERROR,
            NGINX_ERROR_1,
            {
                'year': '2020', 'month': '03', 'day': '21',
                'hour': '23', 'minute': '30', 'second': '24', 'microsecond': None,
                'timezone': None,
                'level': 'crit',
                'proc_id': '30016',
                'thread_id': '0',
                'connection_counter': '4',
                'message': 'stat() "/var/www/html/index.php" failed (13: Permission denied), client: 127.0.0.1, server: example.com, request: "GET /index.php HTTP/1.1", host: "example.com"',
            },
        ),
    ),
)
def test_molecule_nginx_error(
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
