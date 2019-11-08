from pathlib import Path

import pytest

from tagfiles import ArtistRoles, NonIntegerTag, TagFile

FAKE_ALBUM_DIR = (Path(__file__) / '../fakelib/New Album').resolve()


@pytest.mark.parametrize(
    'filepath, track_num',
    [
        ('track1.flac', '1'),
        ('track2.m4a', '2'),
        ('track3.mp3', '3'),
        ('track4.vorbis.ogg', '4'),
        ('track5.opus.ogg', '5'),
    ],
)
def test_getters(filepath, track_num):
    tf = TagFile(FAKE_ALBUM_DIR / filepath)
    assert tf.track_number == track_num
    assert tf.title == f'Track {track_num}'

    assert tf.album == 'A Cool Album'
    assert tf.artist_album == ['Artist A', 'Artist B']
    assert tf.catalog_number == 'COL01'
    assert tf.release_type == 'Album'
    assert tf.comment == 'A Good Album ~reviewer'
    assert tf.date.year == 1990
    assert tf.date.date == '1990-02-05'
    assert tf.disc_number == '1'
    assert tf.disc_total == '1'
    assert tf.genre == ['Electronic', 'House']
    assert tf.label == 'A Cool Label'
    assert tf.track_total == '5'
    assert tf.version == 'Artist AB Remix'

    assert tf.artist == {
        ArtistRoles.MAIN: ['Artist A'],
        ArtistRoles.FEATURE: ['Artist C'],
        ArtistRoles.REMIXER: ['Artist AB', 'Artist BC'],
        ArtistRoles.PRODUCER: ['Artist CD', 'Artist DE'],
        ArtistRoles.COMPOSER: ['Artist EF', 'Artist FG'],
        ArtistRoles.CONDUCTOR: ['Artist GH', 'Artist HI'],
        ArtistRoles.DJMIXER: ['Artist IJ', 'Artist JK'],
    }


def test_m4a_noninteger_tracks():
    tf = TagFile(FAKE_ALBUM_DIR / 'track2.m4a')
    with pytest.raises(NonIntegerTag):
        tf.track_number = 'A1'


@pytest.mark.parametrize(
    'filepath',
    [
        'track1.flac',
        'track2.m4a',
        'track3.mp3',
        'track4.vorbis.ogg',
        'track5.opus.ogg',
    ],
)
def test_setters(filepath):
    tf = TagFile(FAKE_ALBUM_DIR / filepath)
    tf.track_number = 10
    assert tf.track_number == '10'
    tf.title = 'New Title'
    assert tf.title == f'New Title'
    tf.album = 'New Album'
    assert tf.album == 'New Album'
    tf.artist_album = ['New Artist A', 'New Artist B']
    assert tf.artist_album == ['New Artist A', 'New Artist B']
    tf.catalog_number = 'NEW01'
    assert tf.catalog_number == 'NEW01'
    tf.release_type = 'EP'
    assert tf.release_type == 'EP'
    tf.comment = 'A New Album ~reviewer'
    assert tf.comment == 'A New Album ~reviewer'
    tf.date = '2018-12-25'
    assert tf.date.year == 2018
    assert tf.date.date == '2018-12-25'
    tf.disc_number = 5
    assert tf.disc_number == '5'
    tf.disc_total = 5
    assert tf.disc_total == '5'
    tf.genre = ['Avantgarde', 'Synthpop']
    assert tf.genre == ['Avantgarde', 'Synthpop']
    tf.label = 'A New Label'
    assert tf.label == 'A New Label'
    tf.track_total = 50
    assert tf.track_total == '50'
    tf.version = 'New Artist AB Remix'
    assert tf.version == 'New Artist AB Remix'

    tf.artist_main = ['New Artist A']
    tf.artist_feature = ['New Artist C']
    tf.artist_remixer = ['New Artist AB', 'New Artist BC']
    tf.artist_producer = ['New Artist CD', 'New Artist DE']
    tf.artist_composer = ['New Artist EF', 'New Artist FG']
    tf.artist_conductor = ['New Artist GH', 'New Artist HI']
    tf.artist_djmixer = ['New Artist IJ', 'New Artist JK']

    assert tf.artist == {
        ArtistRoles.MAIN: ['New Artist A'],
        ArtistRoles.FEATURE: ['New Artist C'],
        ArtistRoles.REMIXER: ['New Artist AB', 'New Artist BC'],
        ArtistRoles.PRODUCER: ['New Artist CD', 'New Artist DE'],
        ArtistRoles.COMPOSER: ['New Artist EF', 'New Artist FG'],
        ArtistRoles.CONDUCTOR: ['New Artist GH', 'New Artist HI'],
        ArtistRoles.DJMIXER: ['New Artist IJ', 'New Artist JK'],
    }


@pytest.mark.parametrize(
    'filepath',
    [
        'track1.flac',
        'track2.m4a',
        'track3.mp3',
        'track4.vorbis.ogg',
        'track5.opus.ogg',
    ],
)
def test_setters_str_list_intermix(filepath):
    tf = TagFile(FAKE_ALBUM_DIR / filepath)
    tf.track_number = [10]
    assert tf.track_number == '10'
    tf.title = ['New Title']
    assert tf.title == f'New Title'
    tf.album = ['New Album']
    assert tf.album == 'New Album'
    tf.artist_album = r'New Artist A \\ New Artist B'
    assert tf.artist_album == ['New Artist A', 'New Artist B']
    tf.catalog_number = ['NEW01']
    assert tf.catalog_number == 'NEW01'
    tf.release_type = ['EP']
    assert tf.release_type == 'EP'
    tf.comment = ['A New Album ~reviewer']
    assert tf.comment == 'A New Album ~reviewer'
    tf.date = ['2018-12-25']
    assert tf.date.year == 2018
    assert tf.date.date == '2018-12-25'
    tf.disc_number = [5]
    assert tf.disc_number == '5'
    tf.disc_total = [5]
    assert tf.disc_total == '5'
    tf.genre = r'Avantgarde \\ Synthpop'
    assert tf.genre == ['Avantgarde', 'Synthpop']
    tf.label = ['A New Label']
    assert tf.label == 'A New Label'
    tf.track_total = [50]
    assert tf.track_total == '50'
    tf.version = ['New Artist AB Remix']
    assert tf.version == 'New Artist AB Remix'

    tf.artist_main = 'New Artist A'
    tf.artist_feature = 'New Artist C'
    tf.artist_remixer = 'New Artist AB; New Artist BC'
    tf.artist_producer = r'New Artist CD \\ New Artist DE'
    tf.artist_composer = 'New Artist EF; New Artist FG'
    tf.artist_conductor = r'New Artist GH \\ New Artist HI'
    tf.artist_djmixer = 'New Artist IJ / New Artist JK'

    assert tf.artist == {
        ArtistRoles.MAIN: ['New Artist A'],
        ArtistRoles.FEATURE: ['New Artist C'],
        ArtistRoles.REMIXER: ['New Artist AB', 'New Artist BC'],
        ArtistRoles.PRODUCER: ['New Artist CD', 'New Artist DE'],
        ArtistRoles.COMPOSER: ['New Artist EF', 'New Artist FG'],
        ArtistRoles.CONDUCTOR: ['New Artist GH', 'New Artist HI'],
        ArtistRoles.DJMIXER: ['New Artist IJ', 'New Artist JK'],
    }
