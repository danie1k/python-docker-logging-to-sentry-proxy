import re

from src import _base, add_context, add_regex


class Atom(_base.BaseAtom):
    NGINX_ERROR_DATE = r'(?P<year>[12]\d{3})/(?P<month>0\d|1[012])/(?P<day>[012]\d|3[01])'
    NGINX_CID = r'(?P<connection_counter>[0-9]+)'


# https://stackoverflow.com/a/26125951
# https://github.com/phusion/nginx/blob/master/src/core/ngx_log.c
NGINX_ERROR = re.compile((
    r'{NGINX_ERROR_DATE}\s{TIME}{TIMEZONE}?\s\[{LEVEL}\]\s{PROC_ID}#{THREAD_ID}:\s'
    r'(\*{NGINX_CID}\s)?{MESSAGE}$'
).format(**Atom.asdict()))


add_regex(NGINX_ERROR)
add_context('nginx', ['cid'])
