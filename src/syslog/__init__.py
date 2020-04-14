from src import add_context, add_regex

from .regex import RFC5424


add_regex(RFC5424)

add_context('syslog', [
    'appname',
    'hostname',
    'msgid',
    'severity',
    'structured_data',
    'version',
])

add_context('docker', [
    'container_id',
    'container_name',
    'daemon_name',
    'image_id',
    'image_name',
])
