import re
from collections import namedtuple
from typing import Dict, Optional

import pytest

from src.mariadb_mysql import regex

TestCase = namedtuple('TestCase', 'given_expression given_string expected_result')


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # MYSQL_ERR_CODE
        TestCase(regex.Atom.MYSQL_ERR_CODE, 'ER_SERVER_SHUTDOWN_COMPLETE', {'err_code': 'ER_SERVER_SHUTDOWN_COMPLETE'}),
        TestCase(regex.Atom.MYSQL_ERR_CODE, 'MY-000031', {'err_code': 'MY-000031'}),
        TestCase(regex.Atom.MYSQL_ERR_CODE, '000031', {'err_code': '000031'}),
        TestCase(regex.Atom.MYSQL_ERR_CODE, 'MY-31', {'err_code': 'MY-31'}),
        TestCase(regex.Atom.MYSQL_ERR_CODE, '31', {'err_code': '31'}),
        TestCase(regex.Atom.MYSQL_ERR_CODE, 'ERROR 1052', None),
        # MYSQL_SUBSYSTEM
        TestCase(regex.Atom.MYSQL_SUBSYSTEM, 'InnoDB', {'subsystem': 'InnoDB'}),
        TestCase(regex.Atom.MYSQL_SUBSYSTEM, 'Server', {'subsystem': 'Server'}),

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


MYSQL_1 = '2020-03-22T12:35:47.538083Z 0 [Note] [MY-012487] [InnoDB] InnoDB: DDL log recovery : begin'
MYSQL_2 = '2020-03-22T12:35:47.538083Z 4 [Warning] [10051] [Server] Event Scheduler: scheduler thread started with id 4'
MYSQL_3 = '2020-03-22T12:35:47.538083Z 0 [Note] [InnoDB] InnoDB: DDL log recovery : begin'
MYSQL_4 = '2020-03-22T12:35:47.538083Z 0 [Note] [MY-012487] InnoDB: DDL log recovery : begin'
MYSQL_5 = '2020-03-22T12:35:47.538083Z 0 [Note] InnoDB: DDL log recovery : begin'

MARIADB_1 = '2020-03-22 12:35:47 140310100753288 [Note] InnoDB:  Percona XtraDB (http://www.percona.com) 5.6.38-83.0 started'


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # MySQL >= 8.0 (full)
        TestCase(
            regex.MYSQL,
            MYSQL_1,
            {
                'year': '2020', 'month': '03', 'day': '22',
                'hour': '12', 'minute': '35', 'second': '47', 'microsecond': '538083',
                'timezone': 'Z',
                'thread_id': '0',
                'priority': 'Note',
                'err_code': 'MY-012487',
                'subsystem': 'InnoDB',
                'message': 'InnoDB: DDL log recovery : begin',
            },
        ),
        TestCase(
            regex.MYSQL,
            MYSQL_2,
            {
                'year': '2020', 'month': '03', 'day': '22',
                'hour': '12', 'minute': '35', 'second': '47', 'microsecond': '538083',
                'timezone': 'Z',
                'thread_id': '4',
                'priority': 'Warning',
                'err_code': '10051',
                'subsystem': 'Server',
                'message': 'Event Scheduler: scheduler thread started with id 4',
            },
        ),
        # MySQL >= 8.0 (variations with missing parts)
        TestCase(
            regex.MYSQL,
            MYSQL_3,
            {
                'year': '2020', 'month': '03', 'day': '22',
                'hour': '12', 'minute': '35', 'second': '47', 'microsecond': '538083',
                'timezone': 'Z',
                'thread_id': '0',
                'priority': 'Note',
                'err_code': None,
                'subsystem': 'InnoDB',
                'message': 'InnoDB: DDL log recovery : begin',
            },
        ),
        TestCase(
            regex.MYSQL,
            MYSQL_4,
            {
                'year': '2020', 'month': '03', 'day': '22',
                'hour': '12', 'minute': '35', 'second': '47', 'microsecond': '538083',
                'timezone': 'Z',
                'thread_id': '0',
                'priority': 'Note',
                'err_code': 'MY-012487',
                'subsystem': None,
                'message': 'InnoDB: DDL log recovery : begin',
            },
        ),
        # MySQL < 8.0
        TestCase(
            regex.MYSQL,
            MYSQL_5,
            {
                'year': '2020', 'month': '03', 'day': '22',
                'hour': '12', 'minute': '35', 'second': '47', 'microsecond': '538083',
                'timezone': 'Z',
                'thread_id': '0',
                'priority': 'Note',
                'err_code': None,
                'subsystem': None,
                'message': 'InnoDB: DDL log recovery : begin',
            },
        ),
        # MariaDB >= 10.1.5
        TestCase(
            regex.MYSQL,
            MARIADB_1,
            {
                'year': '2020', 'month': '03', 'day': '22',
                'hour': '12', 'minute': '35', 'second': '47', 'microsecond': None,
                'timezone': None,
                'thread_id': '140310100753288',
                'priority': 'Note',
                'err_code': None,
                'subsystem': None,
                'message': 'InnoDB:  Percona XtraDB (http://www.percona.com) 5.6.38-83.0 started',
            },
        ),
    ),
)
def test_molecule(
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
