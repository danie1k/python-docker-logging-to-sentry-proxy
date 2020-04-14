import enum
import logging


class MySQLPriority2Logging(enum.IntEnum):
    INFORMATION = logging.INFO
    NOTE = logging.INFO
    WARNING = logging.WARN
    ERROR = logging.ERROR


class NginxLevel2Logging(enum.IntEnum):
    # https://github.com/phusion/nginx/blob/master/src/core/ngx_log.h
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    NOTICE = logging.WARN
    WARN = logging.WARN
    ERROR = logging.ERROR
    CRIT = logging.CRITICAL
    ALERT = logging.CRITICAL
    EMERG = logging.CRITICAL
