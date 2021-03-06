import re
from collections import namedtuple
from typing import Dict, Optional

import pytest

from src.syslog import regex

TestCase = namedtuple('TestCase', 'given_expression given_string expected_result')


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # Atom.RFC5424_SEVERITY
        TestCase(regex.Atom.RFC5424_SEVERITY, '0', {'severity': '0'}),
        TestCase(regex.Atom.RFC5424_SEVERITY, '83', {'severity': '83'}),
        TestCase(regex.Atom.RFC5424_SEVERITY, '191', {'severity': '191'}),
        # Atom.RFC5424_VERSION
        TestCase(regex.Atom.RFC5424_VERSION, '1', {'version': '1'}),
        TestCase(regex.Atom.RFC5424_VERSION, '42', {'version': '42'}),
        # Atom.RFC5424_HOSTNAME
        # Atom.RFC5424_APPNAME
        # Atom.RFC5424_MSGID
        ### DOCKER:d8e210ec875a0871880e004f8fc37e0bf56140093155b8d55aec93d9dc66a53e~mariadb_1~sha256:20da7ed64a1e90fbee45ce9c14a4145fda05182b3ca712b8bf6fe5044d5bf6e6~million12/mariadb~docker
        # Atom.RFC5424_STRUCTURED_DATA
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


RFC5424_1 = f'<30>1 2020-03-22T12:35:47.385660+02:00 host.localdomain 6e8ef9a56b54 927 6e8ef9a56b54 - 2020-03-22T12:35:47.538083Z 0 [Note] [MY-012487] [InnoDB] InnoDB: DDL log recovery : begin'
RFC5424_2 = '<165>1 2003-10-11T22:14:15.003Z mymachine.example.com evntslog - ID47 [exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"] BOM An application event log entry...'
RFC5424_3 = '<165>1 2003-10-11T22:14:15.003Z mymachine.example.com evntslog - ID47 [exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"][examplePriority@32473 class="high"]'


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # Syslog (rfc5424micro) from Docker container
        TestCase(
            regex.RFC5424,
            RFC5424_1,
            {
                'severity': '30', 'version': '1',
                'year': '2020', 'month': '03', 'day': '22',
                'hour': '12', 'minute': '35', 'second': '47', 'microsecond': '385660',
                'timezone': '+02:00',
                'hostname': 'host.localdomain',
                'appname': '6e8ef9a56b54',
                'proc_id': '927',
                'msgid': '6e8ef9a56b54',
                'structured_data': '-',
                'message': '2020-03-22T12:35:47.538083Z 0 [Note] [MY-012487] [InnoDB] InnoDB: DDL log recovery : begin',
                'container_id': None, 'container_name': None, 'daemon_name': None, 'image_id': None, 'image_name': None,
            }
        ),
        # Syslog example 3 - with STRUCTURED-DATA
        TestCase(
            regex.RFC5424,
            RFC5424_2,
            {
                'severity': '165', 'version': '1',
                'year': '2003', 'month': '10', 'day': '11',
                'hour': '22', 'minute': '14', 'second': '15', 'microsecond': '003',
                'timezone': 'Z',
                'hostname': 'mymachine.example.com',
                'appname': 'evntslog',
                'proc_id': '-',
                'msgid': 'ID47',
                'structured_data': '[exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"]',
                'message': 'BOM An application event log entry...',
                'container_id': None, 'container_name': None, 'daemon_name': None, 'image_id': None, 'image_name': None,
            }
        ),
        # Syslog example 4 - STRUCTURED-DATA Only
        TestCase(
            regex.RFC5424,
            RFC5424_3,
            {
                'severity': '165', 'version': '1',
                'year': '2003', 'month': '10', 'day': '11',
                'hour': '22', 'minute': '14', 'second': '15', 'microsecond': '003',
                'timezone': 'Z',
                'hostname': 'mymachine.example.com',
                'appname': 'evntslog',
                'proc_id': '-',
                'msgid': 'ID47',
                'structured_data': '[exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"][examplePriority@32473 class="high"]',
                'message': None,
                'container_id': None, 'container_name': None, 'daemon_name': None, 'image_id': None, 'image_name': None,
            }
        ),
    ),
)
def test_molecule_rfc5424(
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
