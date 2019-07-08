import re
from enum import Enum


class ArtistRoles(Enum):
    MAIN = 1
    FEATURE = 2
    REMIXER = 3
    PRODUCER = 4
    COMPOSER = 5
    CONDUCTOR = 6
    DJMIXER = 7


class TagDate:
    def __init__(self, value):
        value = str(value)  # ID3TimeStamp object sometimes comes through.
        self.year = self.date = None
        if value:
            if re.match(r'\d{4}$', value):
                self.year = int(value)
            elif re.match(r'\d{4}-\d{2}-\d{2}$', value):
                self.date = value
                self.year = int(self.date[:4])


def unpack_first(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value


def pack_list(value):
    return value if isinstance(value, list) else [value]
