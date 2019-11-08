from mutagen import id3
from mutagen.id3 import ID3, IPLS, TIPL
from mutagen.mp3 import MP3

from tagfiles._common import unpack_first

from .base import BaseTag

# TODO: Handle v3 and v4 differences wrt TIPL and IPLS by checking type.


class MP3Tag(BaseTag):

    extensions = ('.mp3',)
    mutagen_type = MP3
    tags_type = ID3

    tags_title = ['TIT2']
    tags_version = ['TXXX:VERSION']
    tags_date = ['TDRC', 'TYER']
    tags_track_number = ['TRCK']
    tags_disc_number = ['TPOS']
    tags_album = ['TALB']
    tags_genre = ['TCON']
    tags_label = ['TPUB']
    tags_catalog_number = ['TXXX:CATALOGNUMBER']
    tags_release_type = ['TXXX:RELEASETYPE']
    tags_comment = ['COMM', 'COMM::XXX']

    tags_artist_album = ['TPE2']
    tags_artist_main = ['TPE1']
    tags_artist_remixer = ['TPE4']
    tags_artist_producer = 'producer'
    tags_artist_composer = ['TCOM']
    tags_artist_conductor = ['TPE3']
    tags_artist_djmixer = 'DJ-mix'

    def get_tag(self, fields):
        for t in fields:
            if t in self.mut.tags:
                try:
                    return str(self.mut.tags[t].text[0])
                except (KeyError, ValueError):
                    pass

    def set_tag(self, fields, value):
        if fields:
            if isinstance(value, list):
                value = r' \\ '.join(str(v) for v in value)
            try:  # Assume the tag is a special tag with a description first.
                key, desc = fields[0].split(':', 1)
                kwargs = dict(desc=desc, text=value)
                old_frames = [
                    f
                    for f in self.mut.tags.getall(key)
                    if getattr(f, 'desc', None) != desc
                ]
                self.mut.tags.delall(key)
                for f in old_frames:
                    self.mut.tags.add(f)
            except ValueError:  # The tag isn't a special tag.
                key = fields[0]
                kwargs = dict(text=value)
                self.mut.tags.delall(key)
            frame = getattr(id3, key)(**kwargs)
            self.mut.tags.add(frame)

    def get_paired_text_frame(self, role):
        _, _, full_frame = self._get_full_paired_text_frame()
        if not full_frame:
            return []
        return self._split_values(
            [p[1] for p in full_frame.people if p[0].lower() == role.lower()]
        )

    def _get_full_paired_text_frame(self):
        for tag, frame in {'TIPL': TIPL, 'IPLS': IPLS}.items():
            try:
                return tag, frame, self.mut.tags[tag]
            except KeyError:
                pass
        return 'TIPL', TIPL, None

    def set_paired_text_frame(self, role, value):
        if isinstance(value, list):
            value = r' \\ '.join(str(v) for v in value)

        key, frame_type, full_frame = self._get_full_paired_text_frame()
        if full_frame:
            people = [
                p for p in full_frame.people if p[0].lower() != role.lower()
            ]
        else:
            people = []

        frame = frame_type(encoding=3, people=people + [[role, value]])
        self.mut.tags.delall(key)
        self.mut.tags.add(frame)

    def get_list(self, fields):
        for t in fields:
            if t in self.mut.tags:
                try:
                    return self._split_values(
                        [self._decode_tag(s) for s in self.mut.tags[t]]
                    )
                except KeyError:
                    pass
        return []

    def set_list(self, fields, values):
        self.set_tag(fields, values)

    @property
    def track_number(self):
        return get_num(self.get_tag(self.tags_track_number))

    @track_number.setter
    def track_number(self, value):
        self.set_tag(
            fields=self.tags_track_number,
            value=change_tag_num(self.get_tag(self.tags_track_number), value),
        )

    @property
    def track_total(self):
        return get_total(self.get_tag(self.tags_track_number))

    @track_total.setter
    def track_total(self, value):
        self.set_tag(
            fields=self.tags_track_number,
            value=change_tag_total(
                self.get_tag(self.tags_track_number), value
            ),
        )

    @property
    def disc_number(self):
        return get_num(self.get_tag(self.tags_disc_number))

    @disc_number.setter
    def disc_number(self, value):
        self.set_tag(
            fields=self.tags_disc_number,
            value=change_tag_num(self.get_tag(self.tags_disc_number), value),
        )

    @property
    def disc_total(self):
        return get_total(self.get_tag(self.tags_disc_number))

    @disc_total.setter
    def disc_total(self, value):
        self.set_tag(
            fields=self.tags_disc_number,
            value=change_tag_total(self.get_tag(self.tags_disc_number), value),
        )

    @property
    def artist_producer(self):
        return self.get_paired_text_frame(self.tags_artist_producer)

    @artist_producer.setter
    def artist_producer(self, values):
        self.set_paired_text_frame(self.tags_artist_producer, values)

    @property
    def artist_djmixer(self):
        return self.get_paired_text_frame(self.tags_artist_djmixer)

    @artist_djmixer.setter
    def artist_djmixer(self, values):
        self.set_paired_text_frame(self.tags_artist_djmixer, values)


def get_num(tag):
    try:
        return tag.split('/')[0]
    except (IndexError, AttributeError):
        return tag


def get_total(tag):
    try:
        return tag.split('/')[1]
    except (IndexError, AttributeError):
        return None


def change_tag_num(current_tag, value):
    value = unpack_first(value)
    total = get_total(current_tag)
    return f'{value}/{total}' if total else str(value)


def change_tag_total(current_tag, value):
    num = get_num(current_tag)
    return f'{num}/{unpack_first(value)}'
