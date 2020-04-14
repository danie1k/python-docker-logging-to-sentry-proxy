import re


class AsdictMixin:
    @classmethod
    def asdict(cls):
        return {k: v for k, v in cls.__dict__.items() if not k.startswith('_')}


class Atom(AsdictMixin):
    # https://regex101.com/library/Wgbxn2
    RFC5424_SEVERITY = r'(?P<severity>\d{1,3})'
    RFC5424_VERSION = r'(?P<version>\d{1,2})'
    RFC5424_HOSTNAME = r'(?P<hostname>\S{1,255})'
    RFC5424_APPNAME = r'(?P<appname>[^\s]+)'
    # tag: "DOCKER:{{.FullID}}~{{.Name}}~{{.ImageFullID}}~{{.ImageName}}~{{.DaemonName}}"
    RFC5424_MSGID = r'(?P<msgid>DOCKER:(?P<container_id>[a-z0-9]+)~(?P<container_name>\S+)~(?P<image_id>[a-z0-9:]+)~(?P<image_name>\S+)~(?P<daemon_name>\S+)|\S+)'
    RFC5424_STRUCTURED_DATA = r'(?P<structured_data>-|(?:\[.+?(?<!\\)\])+)'


class Molecule(AsdictMixin):
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
