import re
from collections import defaultdict
from itertools import chain

from tagfiles._common import ArtistRoles, TagDate, pack_list, unpack_first


class BaseTag:

    extension = None
    mutagen_type = None
    tags_type = None

    tags_title = []
    tags_version = []
    tags_date = []
    tags_track_number = []
    tags_track_total = []
    tags_disc_number = []
    tags_disc_total = []
    tags_album = []
    tags_genre = []
    tags_label = []
    tags_catalog_number = []
    tags_release_type = []
    tags_comment = []

    tags_artist_album = []
    tags_artist_main = []
    tags_artist_remixer = []
    tags_artist_producer = []
    tags_artist_composer = []
    tags_artist_conductor = []
    tags_artist_djmixer = []

    def __init__(self, filepath, mut):
        self.path = filepath
        self.mut = mut
        if self.mut.tags is None:
            self.create_tags_object()
        self.save = self.mut.save

    def create_tags_object(self):
        self.mut.tags = self.tags_type()

    def __repr__(self):
        return f'<{self.__class__.__name__} object of {self.path}>'

    @classmethod
    def get_allowed_extensions(cls):
        if not hasattr(cls, '_allowed_extensions'):
            cls._allowed_extensions = defaultdict(list)
            for subcls in cls.__subclasses__():
                for ext in subcls.extensions:
                    cls._allowed_extensions[ext].append(subcls)
        return cls._allowed_extensions

    @staticmethod
    def _decode_tag(tag):
        if isinstance(tag, bytes):
            return tag.decode('utf-8')
        elif isinstance(tag, tuple):
            return tag
        return str(tag)

    def _split_values(self, values):
        return list(
            chain.from_iterable(re.split(r' \\\\ | / |; ', v) for v in values)
        )

    def get_tag(self, fields):
        for t in fields:
            if t in self.mut.tags:
                try:
                    value = unpack_first(self.mut.tags[t])
                    return self._decode_tag(value)
                except (KeyError, IndexError):
                    pass

    def set_tag(self, fields, value, cast_to_str=True):
        if isinstance(value, list):
            if cast_to_str:
                value = r' \\ '.join(str(v) for v in value)
            else:
                value = value[0]
        if fields:
            self.mut.tags[fields[0]] = str(value) if cast_to_str else value

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

    def set_list(self, fields, values, cast_to_str=True):
        if fields:
            self.mut.tags[fields[0]] = [
                str(v) if cast_to_str else v for v in pack_list(values)
            ]

    @property
    def title(self):
        return self.get_tag(self.tags_title)

    @title.setter
    def title(self, value):
        self.set_tag(self.tags_title, value)

    @property
    def version(self):
        return self.get_tag(self.tags_version)

    @version.setter
    def version(self, value):
        self.set_tag(self.tags_version, value)

    @property
    def date(self):
        return TagDate(self.get_tag(self.tags_date))

    @date.setter
    def date(self, value):
        self.set_tag(self.tags_date, value)

    @property
    def track_number(self):
        return self.get_tag(self.tags_track_number)

    @track_number.setter
    def track_number(self, value):
        self.set_tag(self.tags_track_number, value)

    @property
    def track_total(self):
        return self.get_tag(self.tags_track_total)

    @track_total.setter
    def track_total(self, value):
        self.set_tag(self.tags_track_total, value)

    @property
    def disc_number(self):
        return self.get_tag(self.tags_disc_number)

    @disc_number.setter
    def disc_number(self, value):
        self.set_tag(self.tags_disc_number, value)

    @property
    def disc_total(self):
        return self.get_tag(self.tags_disc_total)

    @disc_total.setter
    def disc_total(self, value):
        self.set_tag(self.tags_disc_total, value)

    @property
    def album(self):
        return self.get_tag(self.tags_album)

    @album.setter
    def album(self, value):
        self.set_tag(self.tags_album, value)

    @property
    def genre(self):
        return self.get_list(self.tags_genre)

    @genre.setter
    def genre(self, values):
        self.set_list(self.tags_genre, values)

    @property
    def label(self):
        return self.get_tag(self.tags_label)

    @label.setter
    def label(self, value):
        self.set_tag(self.tags_label, value)

    @property
    def catalog_number(self):
        return self.get_tag(self.tags_catalog_number)

    @catalog_number.setter
    def catalog_number(self, value):
        self.set_tag(self.tags_catalog_number, value)

    @property
    def release_type(self):
        return self.get_tag(self.tags_release_type)

    @release_type.setter
    def release_type(self, value):
        self.set_tag(self.tags_release_type, value)

    @property
    def comment(self):
        return self.get_tag(self.tags_comment)

    @comment.setter
    def comment(self, value):
        self.set_tag(self.tags_comment, value)

    @property
    def artist_album(self):
        return self.get_list(self.tags_artist_album)

    @artist_album.setter
    def artist_album(self, values):
        self.set_list(self.tags_artist_album, values)

    @property
    def artist(self):
        return {
            ArtistRoles.MAIN: self.artist_main,
            ArtistRoles.FEATURE: self.artist_feature,
            ArtistRoles.REMIXER: self.artist_remixer,
            ArtistRoles.PRODUCER: self.artist_producer,
            ArtistRoles.COMPOSER: self.artist_composer,
            ArtistRoles.CONDUCTOR: self.artist_conductor,
            ArtistRoles.DJMIXER: self.artist_djmixer,
        }

    @property
    def artist_main(self):
        return [
            a
            for a in self.get_list(self.tags_artist_main)
            if not a.startswith('feat. ')
        ]

    @artist_main.setter
    def artist_main(self, values):
        self.set_list(
            self.tags_artist_main,
            pack_list(values) + [f'feat. {a}' for a in self.artist_feature],
        )

    @property
    def artist_feature(self):
        return [
            re.sub(r'^feat\. ', '', a)
            for a in self.get_list(self.tags_artist_main)
            if a.startswith('feat. ')
        ]

    @artist_feature.setter
    def artist_feature(self, values):
        self.set_list(
            self.tags_artist_main,
            [f'feat. {v}' for v in pack_list(values)] + self.artist_main,
        )

    @property
    def artist_remixer(self):
        return self.get_list(self.tags_artist_remixer)

    @artist_remixer.setter
    def artist_remixer(self, values):
        self.set_list(self.tags_artist_remixer, values)

    @property
    def artist_producer(self):
        return self.get_list(self.tags_artist_producer)

    @artist_producer.setter
    def artist_producer(self, values):
        self.set_list(self.tags_artist_producer, values)

    @property
    def artist_composer(self):
        return self.get_list(self.tags_artist_composer)

    @artist_composer.setter
    def artist_composer(self, values):
        self.set_list(self.tags_artist_composer, values)

    @property
    def artist_conductor(self):
        return self.get_list(self.tags_artist_conductor)

    @artist_conductor.setter
    def artist_conductor(self, values):
        self.set_list(self.tags_artist_conductor, values)

    @property
    def artist_djmixer(self):
        return self.get_list(self.tags_artist_djmixer)

    @artist_djmixer.setter
    def artist_djmixer(self, values):
        self.set_list(self.tags_artist_djmixer, values)
