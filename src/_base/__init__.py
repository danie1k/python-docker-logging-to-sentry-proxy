
class AsdictMixin:
    @classmethod
    def asdict(cls):
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('_') and key.isupper()
        }


class BaseAtom(AsdictMixin):
    DATE = r'(?P<year>[12]\d{3})-(?P<month>0\d|1[012])-(?P<day>[012]\d|3[01])'
    # https://www.regexpal.com/22
    IP = r'(?P<ip>(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))'
    LEVEL = r'(?P<level>[A-Za-z]+)'
    MESSAGE = r'(?:(?P<message>.+))'
    PROC_ID = r'(?P<proc_id>\S{1,128})'
    THREAD_ID = r'(?P<thread_id>\S{1,128})'
    TIME = (
        r'(?P<hour>[01]\d|2[0-4]):(?P<minute>[0-5]\d):(?P<second>[0-5]\d|60)'
        r'(?:\.(?P<microsecond>\d{1,6}))?'
    )
    TIMEZONE = r'(?P<timezone>Z|[+-](?:[01]\d|2[0-4]):?[0-5]\d)'

