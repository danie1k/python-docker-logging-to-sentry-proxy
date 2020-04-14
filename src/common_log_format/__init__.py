from src import add_context, add_regex

from .regex import HTTPD


add_regex(HTTPD)

add_context('httpd', [
    'authuser',
    'content_size',
    'http_status',
    'referer',
    'user_agent',
    'user_identifier',
])
