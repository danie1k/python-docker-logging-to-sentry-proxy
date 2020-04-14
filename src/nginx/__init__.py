from src import add_context, add_regex

from .regex import NGINX_ERROR


add_regex(NGINX_ERROR)

add_context('nginx', [
    'connection_counter',
])
