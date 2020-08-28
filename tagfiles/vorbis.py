import base64

from mutagen.flac import FLAC, Picture, VCFLACDict
from mutagen.flac import error as FLACError
from mutagen.oggopus import OggOpus, OggOpusVComment
from mutagen.oggvorbis import OggVCommentDict, OggVorbis

from .base import BaseTag


class VorbisTag:
    tags_title = ['title']
    tags_version = ['version']
    tags_date = ['date', 'year']
    tags_track_number = ['tracknumber']
    tags_track_total = ['tracktotal']
    tags_disc_number = ['discnumber']
    tags_disc_total = ['disctotal']
    tags_album = ['album']
    tags_genre = ['genre']
    tags_label = ['organization', 'label', 'recordlabel']
    tags_catalog_number = ['catalognumber']
    tags_release_type = ['releasetype']
    tags_comment = ['comment']

    tags_artist_album = ['albumartist']
    tags_artist_main = ['artist']
    tags_artist_remixer = ['remixer']
    tags_artist_producer = ['producer']
    tags_artist_composer = ['composer']
    tags_artist_conductor = ['conductor']
    tags_artist_djmixer = ['djmixer']

    def create_tags_object(self):
        self.mut.add_tags()

    @property
    def _picture(self):
        if getattr(self, '__picture__', None):
            return self.__picture

        data = (self.mut.get('metadata_block_picture') or [None])[0]
        if data:
            try:
                self.__picture = Picture(base64.b64decode(data))
                return self.__picture
            except FLACError:
                pass

        return None

    @property
    def image_mime(self):
        return self._picture.mime if self._picture else None

    @property
    def image(self):
        return self._picture.data if self._picture else None


class FLACTag(VorbisTag, BaseTag):
    extensions = ('.flac',)
    mutagen_type = FLAC
    tags_type = VCFLACDict


class OggVorbisTag(VorbisTag, BaseTag):
    extensions = ('.ogg',)
    mutagen_type = OggVorbis
    tags_type = OggVCommentDict


class OggOpusTag(VorbisTag, BaseTag):
    extensions = ('.ogg',)
    mutagen_type = OggOpus
    tags_type = OggOpusVComment
