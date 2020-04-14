from src import add_context, add_regex

from .regex import MYSQL


add_regex(MYSQL)

add_context('mysql', [
    'err_code',
    'subsystem',
])
