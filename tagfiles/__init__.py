import os
from pathlib import Path

from mutagen import File

from tagfiles._common import ArtistRoles, TagDate  # noqa
from tagfiles.errors import NonIntegerTag, UnsupportedFileType  # noqa

from . import id3  # noqa
from . import mp4  # noqa
from . import vorbis  # noqa
from .base import BaseTag


def TagFile(filepath):
    if isinstance(filepath, Path):
        filepath = str(filepath.resolve())
    mut = File(filepath)
    ext = os.path.splitext(filepath)[1]
    try:
        allowed_exts = BaseTag.get_allowed_extensions()
        for subcls in allowed_exts[ext]:
            if isinstance(mut, subcls.mutagen_type):
                return subcls(filepath, mut)
    except KeyError:
        pass
    raise UnsupportedFileType
