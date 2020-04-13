import re
from collections import namedtuple
from typing import Dict, Optional

import pytest

from src import regex

TestCase = namedtuple('TestCase', 'given_expression given_string expected_result')


def assert_molecule(
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


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # Atom.DATE
        TestCase(regex.Atom.DATE, '1970-01-01', {'year': '1970', 'month': '01', 'day': '01'}),
        TestCase(regex.Atom.DATE, '2000-02-03', {'year': '2000', 'month': '02', 'day': '03'}),
        TestCase(regex.Atom.DATE, '98-02-03', None),
        TestCase(regex.Atom.DATE, '2000/02-03', None),
        # Atom.TIME
        TestCase(regex.Atom.TIME, '00:00:00', {'hour': '00', 'minute': '00', 'second': '00', 'microsecond': None}),
        TestCase(regex.Atom.TIME, '23:59:59', {'hour': '23', 'minute': '59', 'second': '59', 'microsecond': None}),
        TestCase(regex.Atom.TIME, '00:00:00.000001', {'hour': '00', 'minute': '00', 'second': '00', 'microsecond': '000001'}),
        TestCase(regex.Atom.TIME, '00:00:00.1', {'hour': '00', 'minute': '00', 'second': '00', 'microsecond': '1'}),
        TestCase(regex.Atom.TIME, '00:00:00.100000', {'hour': '00', 'minute': '00', 'second': '00', 'microsecond': '100000'}),
        TestCase(regex.Atom.TIME, '00:00:00.0000001', None),
        # Atom.TIMEZONE
        TestCase(regex.Atom.TIMEZONE, 'Z', {'timezone': 'Z'}),
        TestCase(regex.Atom.TIMEZONE, '+00:00', {'timezone': '+00:00'}),
        TestCase(regex.Atom.TIMEZONE, '-08:00', {'timezone': '-08:00'}),
        TestCase(regex.Atom.TIMEZONE, '+05:30', {'timezone': '+05:30'}),
        TestCase(regex.Atom.TIMEZONE, '+1:00', None),
        TestCase(regex.Atom.TIMEZONE, '00:00', None),
        # Atom.PROC_ID
        TestCase(regex.Atom.PROC_ID, '0345347597345', {'proc_id': '0345347597345'}),
        TestCase(regex.Atom.PROC_ID, '7a4e19c66688', {'proc_id': '7a4e19c66688'}),
        # Atom.THREAD_ID
        TestCase(regex.Atom.THREAD_ID, '0345347597345', {'thread_id': '0345347597345'}),
        TestCase(regex.Atom.THREAD_ID, '7a4e19c66688', {'thread_id': '7a4e19c66688'}),
        # Atom.PRIORITY
        TestCase(regex.Atom.PRIORITY, 'Error', {'priority': 'Error'}),
        TestCase(regex.Atom.PRIORITY, 'INFORMATION', {'priority': 'INFORMATION'}),
        TestCase(regex.Atom.PRIORITY, 'warning', None),
        # Atom.MYSQL_ERR_CODE
        TestCase(regex.Atom.MYSQL_ERR_CODE, '10051', {'err_code': '10051'}),
        TestCase(regex.Atom.MYSQL_ERR_CODE, 'MY-010051', {'err_code': 'MY-010051'}),
        TestCase(regex.Atom.MYSQL_ERR_CODE, 'ERROR 1052', None),
        # Atom.MYSQL_SUBSYSTEM
        TestCase(regex.Atom.MYSQL_SUBSYSTEM, 'InnoDB', {'subsystem': 'InnoDB'}),
        TestCase(regex.Atom.MYSQL_SUBSYSTEM, 'Server', {'subsystem': 'Server'}),
        # Atom.LOG_IP
        TestCase(regex.Atom.LOG_IP, '192.168.1.1', {'ip': '192.168.1.1'}),
        TestCase(regex.Atom.LOG_IP, '000.0000.00.00', None),
        TestCase(regex.Atom.LOG_IP, '912.456.123.123', None),
        # Atom.LOG_RFC931
        TestCase(regex.Atom.LOG_RFC931, '-', {'user_identifier': '-'}),
        TestCase(regex.Atom.LOG_RFC931, 'foo', {'user_identifier': 'foo'}),
        # Atom.LOG_AUTHUSER
        TestCase(regex.Atom.LOG_AUTHUSER, '-', {'authuser': '-'}),
        TestCase(regex.Atom.LOG_AUTHUSER, 'bar', {'authuser': 'bar'}),
        # Atom.LOG_DATE
        TestCase(regex.Atom.LOG_DATE, '10/Oct/2000', {'year': '2000', 'month': 'Oct', 'day': '10'}),
        TestCase(regex.Atom.LOG_DATE, '10/Oct/98', None),
        # Atom.LOG_STATUS
        TestCase(regex.Atom.LOG_STATUS, '101', {'status': '101'}),
        TestCase(regex.Atom.LOG_STATUS, '202', {'status': '202'}),
        TestCase(regex.Atom.LOG_STATUS, '303', {'status': '303'}),
        TestCase(regex.Atom.LOG_STATUS, '505', {'status': '505'}),
        TestCase(regex.Atom.LOG_STATUS, '99', None),
        TestCase(regex.Atom.LOG_STATUS, '700', None),
        # Atom.LOG_BYTES
        TestCase(regex.Atom.LOG_BYTES, '0', {'bytes': '0'}),
        TestCase(regex.Atom.LOG_BYTES, '58973459', {'bytes': '58973459'}),
        # Atom.LOG_REFERER
        TestCase(regex.Atom.LOG_REFERER, '"http://www.example.com/start.html"', {'referer': 'http://www.example.com/start.html'}),
        TestCase(regex.Atom.LOG_REFERER, '"ftps://www.example.com/file.php"', {'referer': 'ftps://www.example.com/file.php'}),
        TestCase(regex.Atom.LOG_REFERER, '"www.example.com"', None),
        # Atom.LOG_USER_AGENT
        TestCase(regex.Atom.LOG_USER_AGENT, '"Mozilla/4.08 [en] (Win98; I ;Nav)"', {'user_agent': 'Mozilla/4.08 [en] (Win98; I ;Nav)'}),
        TestCase(regex.Atom.LOG_USER_AGENT, '"Foo Bar"', {'user_agent': 'Foo Bar'}),
        # Atom.NGINX_ERROR_DATE
        TestCase(regex.Atom.NGINX_ERROR_DATE, '1970/01/01', {'year': '1970', 'month': '01', 'day': '01'}),
        TestCase(regex.Atom.NGINX_ERROR_DATE, '2000/02/03', {'year': '2000', 'month': '02', 'day': '03'}),
        TestCase(regex.Atom.NGINX_ERROR_DATE, '2000-02-03', None),
        # Atom.NGINX_LEVEL
        TestCase(regex.Atom.NGINX_LEVEL, 'emerg', {'level': 'emerg'}),
        TestCase(regex.Atom.NGINX_LEVEL, 'notice', {'level': 'notice'}),
        TestCase(regex.Atom.NGINX_LEVEL, 'DEBUG', None),
        # Atom.NGINX_CID
        TestCase(regex.Atom.NGINX_CID, '0', {'cid': '0'}),
        TestCase(regex.Atom.NGINX_CID, '345', {'cid': '345'}),
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


MYSQL_1 = '2020-03-22T12:35:47.538083Z 0 [Note] [MY-012487] [InnoDB] InnoDB: DDL log recovery : begin'
MYSQL_2 = '2020-03-22T12:35:47.538083Z 4 [Warning] [10051] [Server] Event Scheduler: scheduler thread started with id 4'
MYSQL_3 = '2020-03-22T12:35:47.538083Z 0 [Note] [InnoDB] InnoDB: DDL log recovery : begin'
MYSQL_4 = '2020-03-22T12:35:47.538083Z 0 [Note] [MY-012487] InnoDB: DDL log recovery : begin'
MYSQL_5 = '2020-03-22T12:35:47.538083Z 0 [Note] InnoDB: DDL log recovery : begin'

MARIADB_1 = '2020-03-22 12:35:47 140310100753288 [Note] InnoDB:  Percona XtraDB (http://www.percona.com) 5.6.38-83.0 started'

NGINX_ERROR_1 = '2020/03/21 23:30:24 [crit] 30016#0: *4 stat() "/var/www/html/index.php" failed (13: Permission denied), client: 127.0.0.1, server: example.com, request: "GET /index.php HTTP/1.1", host: "example.com"'

COMMON_LOG_FORMAT_1 = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326'
COMMON_LOG_FORMAT_2 = '127.0.0.1 - - [19/Jan/2005:21:47:11 +0000] "GET /brum.css HTTP/1.1" 304 0'

COMBINED_LOG_FORMAT_1 = '127.0.0.1 - frank [10/Oct/2000:13:55:36 +0130] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/start.html" "Mozilla/4.08 [en] (Win98; I ;Nav)"'


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # MySQL >= 8.0 (full)
        TestCase(
            regex.Molecule.MYSQL,
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
            regex.Molecule.MYSQL,
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
            regex.Molecule.MYSQL,
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
            regex.Molecule.MYSQL,
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
            regex.Molecule.MYSQL,
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
            regex.Molecule.MYSQL,
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
def test_molecule_mysql__positive(
    given_expression: re.Pattern,
    given_string: str,
    expected_result: Optional[Dict[str, str]],
) -> None:
    assert_molecule(
        given_expression=given_expression,
        given_string=given_string,
        expected_result=expected_result,
    )


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        TestCase(
            regex.Molecule.NGINX_ERROR,
            NGINX_ERROR_1,
            {
                'year': '2020', 'month': '03', 'day': '21',
                'hour': '23', 'minute': '30', 'second': '24', 'microsecond': None,
                'timezone': None,
                'level': 'crit',
                'proc_id': '30016',
                'thread_id': '0',
                'cid': '4',
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
    assert_molecule(
        given_expression=given_expression,
        given_string=given_string,
        expected_result=expected_result,
    )


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # Common Log Format
        TestCase(
            regex.Molecule.HTTPD,
            COMMON_LOG_FORMAT_1,
            {
                'ip': '127.0.0.1',
                'user_identifier': '-',
                'authuser': 'frank',
                'year': '2000', 'month': 'Oct', 'day': '10',
                'hour': '13', 'minute': '55', 'second': '36', 'microsecond': None,
                'timezone': '-0700',
                'message': 'GET /apache_pb.gif HTTP/1.0',
                'status': '200',
                'bytes': '2326',
                'referer': None,
                'user_agent': None,
            },
        ),
        TestCase(
            regex.Molecule.HTTPD,
            COMMON_LOG_FORMAT_2,
            {
                'ip': '127.0.0.1',
                'user_identifier': '-',
                'authuser': '-',
                'year': '2005', 'month': 'Jan', 'day': '19',
                'hour': '21', 'minute': '47', 'second': '11', 'microsecond': None,
                'timezone': '+0000',
                'message': 'GET /brum.css HTTP/1.1',
                'status': '304',
                'bytes': '0',
                'referer': None,
                'user_agent': None,
            },
        ),
        # Combined Log Format
        TestCase(
            regex.Molecule.HTTPD,
            COMBINED_LOG_FORMAT_1,
            {
                'ip': '127.0.0.1',
                'user_identifier': '-',
                'authuser': 'frank',
                'year': '2000', 'month': 'Oct', 'day': '10',
                'hour': '13', 'minute': '55', 'second': '36', 'microsecond': None,
                'timezone': '+0130',
                'message': 'GET /apache_pb.gif HTTP/1.0',
                'status': '200',
                'bytes': '2326',
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
    assert_molecule(
        given_expression=given_expression,
        given_string=given_string,
        expected_result=expected_result,
    )


RFC5424_1 = f'<30>1 2020-03-22T12:35:47.385660+02:00 host.localdomain 6e8ef9a56b54 927 6e8ef9a56b54 - {MYSQL_1}'
RFC5424_2 = '<165>1 2003-10-11T22:14:15.003Z mymachine.example.com evntslog - ID47 [exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"] BOM An application event log entry...'
RFC5424_3 = '<165>1 2003-10-11T22:14:15.003Z mymachine.example.com evntslog - ID47 [exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"][examplePriority@32473 class="high"]'


@pytest.mark.parametrize(
    'given_expression, given_string, expected_result', (
        # Syslog (rfc5424micro) from Docker container
        TestCase(
            regex.Molecule.RFC5424,
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
                'message': MYSQL_1,
            }
        ),
        # Syslog example 3 - with STRUCTURED-DATA
        TestCase(
            regex.Molecule.RFC5424,
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
            }
        ),
        # Syslog example 4 -  STRUCTURED-DATA Only
        TestCase(
            regex.Molecule.RFC5424,
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
            }
        ),
    ),
)
def test_molecule_rfc5424(
    given_expression: re.Pattern,
    given_string: str,
    expected_result: Optional[Dict[str, str]],
) -> None:
    assert_molecule(given_expression, given_string, expected_result)
