import pytest

from tagfiles._common import TagDate, pack_list, unpack_first


def test_tag_date_year_only():
    td = TagDate('2010')
    assert td.year == 2010
    assert td.date is None


def test_tag_date_date():
    td = TagDate('2010-10-10')
    assert td.year == 2010
    assert td.date == '2010-10-10'


@pytest.mark.parametrize(
    'value', ['abc', '201-10-30', 'July 20th, 2018', '', None]
)
def test_tag_date_none(value):
    td = TagDate(value)
    assert td.year is td.date is None


@pytest.mark.parametrize('value', ['hi', ['hi']])
def test_unpack_first(value):
    assert 'hi' == unpack_first(value)


@pytest.mark.parametrize('value', ['hi', ['hi']])
def test_pack_list(value):
    assert ['hi'] == pack_list(value)
