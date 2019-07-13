# tagfiles

[![Build Status](https://travis-ci.org/azuline/tagfiles.svg?branch=master)](https://travis-ci.org/azuline/tagfiles)
[![Coverage Status](https://coveralls.io/repos/github/azuline/tagfiles/badge.svg?branch=master)](https://coveralls.io/github/azuline/tagfiles?branch=master)
[![Pypi](https://img.shields.io/pypi/v/tagfiles.svg)](https://pypi.python.org/pypi/tagfiles)
[![Pyversions](https://img.shields.io/pypi/pyversions/tagfiles.svg)](https://pypi.python.org/pypi/tagfiles)

A tagging interface for multiple audio formats and metadata containers.

The supported audio codecs and containers are:

- FLAC in FLAC container
- MP3 in MP3 container
- AAC in MP4 container
- Vorbis in Ogg container
- Opus in Ogg container

Tag mappings are derived from https://picard.musicbrainz.org/docs/mappings/ .

## Usage

```python
>>> from tagfiles import TagFile, ArtistRoles
>>> from pprint import pprint
>>>
>>> tf = TagFile('/home/azuline/02. No Captain.m4a')
>>> print(tf.title)
No Captain
>>> pprint(tf.artist)
{<ArtistRoles.MAIN: 1>: ['Lane 8'],
 <ArtistRoles.FEATURE: 2>: ['Poliça'],
 <ArtistRoles.REMIXER: 3>: [],
 <ArtistRoles.PRODUCER: 4>: [],
 <ArtistRoles.COMPOSER: 5>: [''],
 <ArtistRoles.CONDUCTOR: 6>: [],
 <ArtistRoles.DJMIXER: 7>: []}
>>> print(tf.artist[ArtistRoles.MAIN])
['Lane 8']
>>> print(tf.date.year)
2015
>>> print(tf.date.date)
2015-01-19
>>>
>>> tf.date = '2018-01-19'  # Fixing the date!
>>> print(tf.date.date)
2018-01-19
>>> print(tf.date.year)
2018
>>> tf.save()
>>>
>>> tf = TagFile('/home/azuline/music.txt')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/azuline/devel/tagfiles/tagfiles/__init__.py", line 27, in TagFile
    raise UnsupportedFileType
tagfiles.errors.UnsupportedFileType
```

The TagFile function takes a filepath as a parameter and returns the class
which corresponds to its container. If an unsupported filetype is passed in,
the `UnsupportedFileType` error is raised. Each class presents the same metadata
interface, which have the following attributes:

```python
title: str
version: str
album: str
artist_album: List[str]
catalog_number: str
release_type: str
comment: str
date.year: int
date.date: str
track_number: str
track_total: str
disc_number: str
disc_total: str
genre: List[str]
label: str
artist = {
  ArtistRoles.MAIN: List[str]
  ArtistRoles.FEATURE: List[str]
  ArtistRoles.REMIXER: List[str]
  ArtistRoles.PRODUCER: List[str]
  ArtistRoles.COMPOSER: List[str]
  ArtistRoles.CONDUCTOR: List[str]
  ArtistRoles.DJMIXER: List[str]
}
```

Fields can be edited by setting new values to the attributes of the TagFile.
To edit the date, which is special, assign a string in the format of `%Y-%m-%d`
or `%Y` to the `date` attribute. To save the changes made to the tags, call the
`save()` method.
