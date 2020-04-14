import re


class AsdictMixin:
    @classmethod
    def asdict(cls):
        return {k: v for k, v in cls.__dict__.items() if not k.startswith('_')}


# https://regex101.com/library/Wgbxn2
class Atom(AsdictMixin):
    # https://www.regexpal.com/22
    LOG_RFC931 = r'(?P<user_identifier>-|\S+)'
    LOG_AUTHUSER = r'(?P<authuser>-|\S+)'
    LOG_DATE = r'(?P<day>[012]\d|3[01])/(?P<month>[A-Z][a-z]+)/(?P<year>[12]\d{3})'
    LOG_STATUS = r'(?P<status>[1-5][0-9]{2})'
    LOG_BYTES = r'(?P<bytes>[0-9]+)'
    LOG_REFERER = r'"(?P<referer>([a-z]+://\S+)?)"'
    LOG_USER_AGENT = r'"(?P<user_agent>[^\"]+)"'

    NGINX_ERROR_DATE = r'(?P<year>[12]\d{3})/(?P<month>0\d|1[012])/(?P<day>[012]\d|3[01])'
    NGINX_LEVEL = r'(?P<level>[a-z]+)'
    NGINX_CID = r'(?P<cid>[0-9]+)'

    RFC5424_SEVERITY = r'(?P<severity>\d{1,3})'
    RFC5424_VERSION = r'(?P<version>\d{1,2})'
    RFC5424_HOSTNAME = r'(?P<hostname>\S{1,255})'
    RFC5424_APPNAME = r'(?P<appname>[^\s]+)'
    # tag: "DOCKER:{{.FullID}}~{{.Name}}~{{.ImageFullID}}~{{.ImageName}}~{{.DaemonName}}"
    RFC5424_MSGID = r'(?P<msgid>DOCKER:(?P<container_id>[a-z0-9]+)~(?P<container_name>\S+)~(?P<image_id>[a-z0-9:]+)~(?P<image_name>\S+)~(?P<daemon_name>\S+)|\S+)'
    RFC5424_STRUCTURED_DATA = r'(?P<structured_data>-|(?:\[.+?(?<!\\)\])+)'


class Molecule(AsdictMixin):
    # https://stackoverflow.com/a/26125951
    # https://github.com/phusion/nginx/blob/master/src/core/ngx_log.c
    NGINX_ERROR = re.compile((
        r'{NGINX_ERROR_DATE}\s{TIME}{TIMEZONE}?\s\[{NGINX_LEVEL}\]\s{PROC_ID}#{THREAD_ID}:\s'
        r'(\*{NGINX_CID}\s)?{MESSAGE}$'
    ).format(**Atom.asdict()))

    # Common Log Format
    # Combined Log Format
    HTTPD = re.compile((
        r'^{IP}\s{LOG_RFC931}\s{LOG_AUTHUSER}\s\[{LOG_DATE}:{TIME}(\s{TIMEZONE})?\] '
        r'"{MESSAGE}"\s{LOG_STATUS}\s{LOG_BYTES}'
        r'(\s{LOG_REFERER})?(\s{LOG_USER_AGENT})?$'
    ).format(**Atom.asdict()))

    # https://tools.ietf.org/html/rfc5424
    # https://docs.docker.com/config/containers/logging/syslog/
    RFC5424 = re.compile((
        r'^<{RFC5424_SEVERITY}>{RFC5424_VERSION}\s'
        r'{DATE}T{TIME}{TIMEZONE}?\s'
        r'{RFC5424_HOSTNAME}\s'
        r'{RFC5424_APPNAME}\s'
        r'{PROC_ID}\s'
        r'{RFC5424_MSGID}\s'
        r'{RFC5424_STRUCTURED_DATA}'
        r'(\s{MESSAGE})?$'
    ).format(**Atom.asdict()))
