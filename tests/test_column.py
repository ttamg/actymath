import pandas as pd
from actymath.columns.base import Column
from actymath.calc import register


class TestColumn1(Column):
    column_name = "q(x{life})"
    parameters = {"life": "test"}
    dependencies = []


class TestColumn2(Column):
    column_name = "timestamp"
    parameters = {}
    dependencies = []


def test_column_parse_works_with_kwargs():
    col = "q(x3)"
    result = TestColumn1().parse_column(col)
    assert result[0] == "q(x{life})"
    assert result[1] == {"life": "3"}
    # And now no match
    col = "q(y1)"
    result = TestColumn1().parse_column(col)
    assert result is None
    # Also no match - case sensitive
    col = "Q(x3)"
    result = TestColumn1().parse_column(col)
    assert result is None


def test_column_parse_works_without_kwargs():
    col = "timestamp"
    result = TestColumn2().parse_column(col)
    assert result[0] == "timestamp"
    assert result[1] == {}
    # and no no match
    col = "times"
    result = TestColumn2().parse_column(col)
    assert result is None