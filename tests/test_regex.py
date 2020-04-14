import re
from collections import namedtuple
from typing import Dict, Optional

import pytest

from src import _base

TestCase = namedtuple('TestCase', 'given_expression given_string expected_result')


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # BaseAtom.DATE
        TestCase(_base.BaseAtom.DATE, '1970-01-01', {'year': '1970', 'month': '01', 'day': '01'}),
        TestCase(_base.BaseAtom.DATE, '2000-02-03', {'year': '2000', 'month': '02', 'day': '03'}),
        TestCase(_base.BaseAtom.DATE, '98-02-03', None),
        TestCase(_base.BaseAtom.DATE, '2000/02-03', None),
        # BaseAtom.TIME
        TestCase(_base.BaseAtom.TIME, '00:00:00', {'hour': '00', 'minute': '00', 'second': '00', 'microsecond': None}),
        TestCase(_base.BaseAtom.TIME, '23:59:59', {'hour': '23', 'minute': '59', 'second': '59', 'microsecond': None}),
        TestCase(_base.BaseAtom.TIME, '00:00:00.000001', {'hour': '00', 'minute': '00', 'second': '00', 'microsecond': '000001'}),
        TestCase(_base.BaseAtom.TIME, '00:00:00.1', {'hour': '00', 'minute': '00', 'second': '00', 'microsecond': '1'}),
        TestCase(_base.BaseAtom.TIME, '00:00:00.100000', {'hour': '00', 'minute': '00', 'second': '00', 'microsecond': '100000'}),
        TestCase(_base.BaseAtom.TIME, '00:00:00.0000001', None),
        # BaseAtom.TIMEZONE
        TestCase(_base.BaseAtom.TIMEZONE, 'Z', {'timezone': 'Z'}),
        TestCase(_base.BaseAtom.TIMEZONE, '+00:00', {'timezone': '+00:00'}),
        TestCase(_base.BaseAtom.TIMEZONE, '-08:00', {'timezone': '-08:00'}),
        TestCase(_base.BaseAtom.TIMEZONE, '+05:30', {'timezone': '+05:30'}),
        TestCase(_base.BaseAtom.TIMEZONE, '+1:00', None),
        TestCase(_base.BaseAtom.TIMEZONE, '00:00', None),
        # BaseAtom.PROC_ID
        TestCase(_base.BaseAtom.PROC_ID, '0345347597345', {'proc_id': '0345347597345'}),
        TestCase(_base.BaseAtom.PROC_ID, '7a4e19c66688', {'proc_id': '7a4e19c66688'}),
        # BaseAtom.THREAD_ID
        TestCase(_base.BaseAtom.THREAD_ID, '0345347597345', {'thread_id': '0345347597345'}),
        TestCase(_base.BaseAtom.THREAD_ID, '7a4e19c66688', {'thread_id': '7a4e19c66688'}),
        # BaseAtom.LEVEL
        TestCase(_base.BaseAtom.LEVEL, 'Error', {'level': 'Error'}),
        TestCase(_base.BaseAtom.LEVEL, 'INFORMATION', {'level': 'INFORMATION'}),
        TestCase(_base.BaseAtom.LEVEL, 'warning', {'level': 'warning'}),
        # BaseAtom.IP
        TestCase(_base.BaseAtom.IP, '192.168.1.1', {'ip': '192.168.1.1'}),
        TestCase(_base.BaseAtom.IP, '000.0000.00.00', None),
        TestCase(_base.BaseAtom.IP, '912.456.123.123', None),
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
