from mutagen.mp4 import MP4, MP4Tags

from tagfiles._common import pack_list, unpack_first
from tagfiles.errors import NonIntegerTag

from .base import BaseTag


class AACTag(BaseTag):

    extensions = ('.m4a', '.m4b')
    mutagen_type = MP4
    tags_type = MP4Tags

    tags_title = ['\xa9nam']
    tags_version = ['----:com.apple.iTunes:VERSION']
    tags_date = ['\xa9day']
    tags_track_number = ['trkn']
    tags_disc_number = ['disk']
    tags_album = ['\xa9alb']
    tags_genre = ['\xa9gen']
    tags_label = ['----:com.apple.iTunes:LABEL']
    tags_catalog_number = ['----:com.apple.iTunes:CATALOGNUMBER']
    tags_release_type = ['----:com.apple.iTunes:RELEASETYPE']
    tags_comment = ['\xa9cmt']

    tags_artist_album = ['aART']
    tags_artist_main = ['\xa9ART']
    tags_artist_remixer = ['----:com.apple.iTunes:REMIXER']
    tags_artist_producer = ['----:com.apple.iTunes:PRODUCER']
    tags_artist_composer = ['\xa9wrt']
    tags_artist_conductor = ['----:com.apple.iTunes:CONDUCTOR']
    tags_artist_djmixer = ['----:com.apple.iTunes:DJMIXER']

    @property
    def version(self):
        return self.get_tag(self.tags_version)

    @version.setter
    def version(self, value):
        self.set_tag(
            fields=self.tags_version,
            value=[unpack_first(value).encode('utf-8')],
            cast_to_str=False,
        )

    @property
    def track_number(self):
        return str(get_num(self.get_tag(self.tags_track_number)))

    @track_number.setter
    def track_number(self, value):
        self.set_list(
            fields=self.tags_track_number,
            values=[
                change_tag_num(self.get_tag(self.tags_track_number), value)
            ],
            cast_to_str=False,
        )

    @property
    def track_total(self):
        return str(get_total(self.get_tag(self.tags_track_number)))

    @track_total.setter
    def track_total(self, value):
        self.set_list(
            fields=self.tags_track_number,
            values=[
                change_tag_total(self.get_tag(self.tags_track_number), value)
            ],
            cast_to_str=False,
        )

    @property
    def disc_number(self):
        return str(get_num(self.get_tag(self.tags_disc_number)))

    @disc_number.setter
    def disc_number(self, value):
        self.set_list(
            fields=self.tags_disc_number,
            values=[
                change_tag_num(self.get_tag(self.tags_disc_number), value)
            ],
            cast_to_str=False,
        )

    @property
    def disc_total(self):
        return str(get_total(self.get_tag(self.tags_disc_number)))

    @disc_total.setter
    def disc_total(self, value):
        self.set_list(
            fields=self.tags_disc_number,
            values=[
                change_tag_total(self.get_tag(self.tags_disc_number), value)
            ],
            cast_to_str=False,
        )

    @property
    def label(self):
        return self.get_tag(self.tags_label)

    @label.setter
    def label(self, value):
        self.set_tag(
            fields=self.tags_label,
            value=unpack_first(value).encode('utf-8'),
            cast_to_str=False,
        )

    @property
    def catalog_number(self):
        return self.get_tag(self.tags_catalog_number)

    @catalog_number.setter
    def catalog_number(self, value):
        self.set_tag(
            fields=self.tags_catalog_number,
            value=unpack_first(value).encode('utf-8'),
            cast_to_str=False,
        )

    @property
    def release_type(self):
        return self.get_tag(self.tags_release_type)

    @release_type.setter
    def release_type(self, value):
        self.set_tag(
            fields=self.tags_release_type,
            value=unpack_first(value).encode('utf-8'),
            cast_to_str=False,
        )

    @property
    def artist_remixer(self):
        return self.get_list(self.tags_artist_remixer)

    @artist_remixer.setter
    def artist_remixer(self, values):
        self.set_list(
            fields=self.tags_artist_remixer,
            values=[v.encode('utf-8') for v in pack_list(values)],
            cast_to_str=False,
        )

    @property
    def artist_producer(self):
        return self.get_list(self.tags_artist_producer)

    @artist_producer.setter
    def artist_producer(self, values):
        self.set_list(
            fields=self.tags_artist_producer,
            values=[v.encode('utf-8') for v in pack_list(values)],
            cast_to_str=False,
        )

    @property
    def artist_conductor(self):
        return self.get_list(self.tags_artist_conductor)

    @artist_conductor.setter
    def artist_conductor(self, values):
        self.set_list(
            fields=self.tags_artist_conductor,
            values=[v.encode('utf-8') for v in pack_list(values)],
            cast_to_str=False,
        )

    @property
    def artist_djmixer(self):
        return self.get_list(self.tags_artist_djmixer)

    @artist_djmixer.setter
    def artist_djmixer(self, values):
        self.set_list(
            fields=self.tags_artist_djmixer,
            values=[v.encode('utf-8') for v in pack_list(values)],
            cast_to_str=False,
        )


def get_num(tag):
    try:
        return int(tag[0])
    except (TypeError, IndexError):
        return tag


def get_total(tag):
    try:
        return int(tag[1])
    except (TypeError, IndexError):
        return None


def change_tag_num(current_tag, value):
    try:
        total = get_total(current_tag)
        return (int(unpack_first(value)), total or 0)
    except ValueError:
        raise NonIntegerTag


def change_tag_total(current_tag, value):
    try:
        num = get_num(current_tag)
        return (num, int(unpack_first(value)))
    except ValueError:
        raise NonIntegerTag
