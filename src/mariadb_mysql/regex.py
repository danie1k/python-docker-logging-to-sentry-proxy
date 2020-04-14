import re

from src import _base, add_context, add_regex


class Atom(_base.BaseAtom):
    MYSQL_ERR_CODE = r'(?P<err_code>[A-Z0-9][A-Z0-9-_]+)'
    MYSQL_SUBSYSTEM = r'(?P<subsystem>[A-Z]\S+)'


# https://mariadb.com/kb/en/error-log/#format
# https://dev.mysql.com/doc/refman/8.0/en/error-log-format.html
MYSQL = re.compile((
    r'{DATE}[T|\s]{TIME}{TIMEZONE}?\s'  # timestamp
    r'({THREAD_ID}\s)?\[{PRIORITY}\]\s(\[{MYSQL_ERR_CODE}\]\s)?(\[{MYSQL_SUBSYSTEM}\]\s)?'
    r'{MESSAGE}$'
).format(**Atom.asdict()))


add_regex(MYSQL)
add_context('mysql', ['err_code', 'subsystem'])
