import re
from collections import deque, defaultdict
from typing import Deque, Dict, List, Tuple, Union

__all__ = (
    'add_context',
    'add_regex',
)

__CONTEXT: Dict[str, Deque[str]] = defaultdict(deque)
__REGEX: Deque[re.Pattern] = deque()


def add_context(name: str, keys: Union[List[str], Tuple[str, ...]]) -> None:
    for item in keys:
        if item not in __CONTEXT[item]:
            __CONTEXT[item].append(name)


def add_regex(item: re.Pattern):
    if item not in __REGEX:
        __REGEX.append(item)
