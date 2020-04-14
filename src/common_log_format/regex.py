import re

from src import _base


class Atom(_base.BaseAtom):
    LOG_AUTHUSER = r'(?P<authuser>-|\S+)'
    LOG_CONTENT_SIZE = r'(?P<content_size>[0-9]+)'
    LOG_DATE = r'(?P<day>[012]\d|3[01])/(?P<month>[A-Z][a-z]+)/(?P<year>[12]\d{3})'
    LOG_HTTP_STATUS = r'(?P<http_status>[1-5][0-9]{2})'
    LOG_REFERER = r'"(?P<referer>([a-z]+://\S+)?)"'
    LOG_RFC931 = r'(?P<user_identifier>-|\S+)'
    LOG_USER_AGENT = r'"(?P<user_agent>[^\"]+)"'


# Common Log Format, Combined Log Format
HTTPD = re.compile((
    r'^{IP}\s{LOG_RFC931}\s{LOG_AUTHUSER}\s\[{LOG_DATE}:{TIME}(\s{TIMEZONE})?\] '
    r'"{MESSAGE}"\s{LOG_HTTP_STATUS}\s{LOG_CONTENT_SIZE}'
    r'(\s{LOG_REFERER})?(\s{LOG_USER_AGENT})?$'
).format(**Atom.asdict()))
