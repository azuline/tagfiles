#!/usr/bin/env python
"""
A tagging script used to tag testing files.

Will likely be incorporated into a future test case.
"""

import os

from tagfiles import TagFile

filenames = [
    'track1.flac',
    'track2.m4a',
    'track3.mp3',
    'track4.vorbis.ogg',
    'track5.opus.ogg',
]

for i, filename in enumerate(filenames):
    filename = os.path.join('New Album', filename)
    try:
        tf = TagFile(filename)
        tf.mut.delete()
        tf.mut.save()
    except ValueError:
        print('valueerror')

    tf = TagFile(filename)
    tf.title = f'Track {i + 1}'
    tf.version = 'Artist AB Remix'
    tf.date = '1990-02-05'
    tf.track_number = i + 1
    tf.track_total = len(filenames)
    tf.disc_number = 1
    tf.disc_total = 1
    tf.album = 'A Cool Album'
    tf.genre = ['Electronic', 'House']
    # tf.genre = 'Electronic; House'
    tf.label = 'A Cool Label'
    tf.catalog_number = 'COL01'
    tf.release_type = 'Album'
    tf.comment = 'A Good Album ~reviewer'
    tf.artist_album = ['Artist A', 'Artist B']
    tf.artist_main = ['Artist A']
    tf.artist_feature = ['Artist C']
    tf.artist_remixer = ['Artist AB', 'Artist BC']
    tf.artist_producer = ['Artist CD', 'Artist DE']
    tf.artist_composer = ['Artist EF', 'Artist FG']
    tf.artist_conductor = ['Artist GH', 'Artist HI']
    tf.artist_djmixer = ['Artist IJ', 'Artist JK']
    tf.save()
