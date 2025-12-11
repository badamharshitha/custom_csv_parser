import io
from custom_csv.reader import CustomCsvReader


def test_simple_rows():
    data = "a,b,c\n1,2,3\n"
    f = io.StringIO(data)
    result = list(CustomCsvReader(f))

    assert result == [["a", "b", "c"], ["1", "2", "3"]]


def test_quoted_fields():
    data = 'a,"b, with comma","multi\nline"\n"ok""yes",x,y\n'
    f = io.StringIO(data)
    result = list(CustomCsvReader(f))

    assert result == [["a", "b, with comma", "multi\nline"], ['ok"yes', "x", "y"]]


def test_empty_fields():
    data = "a,,c,\n"
    f = io.StringIO(data)
    result = list(CustomCsvReader(f))

    assert result == [["a", "", "c", ""]]


def test_single_line_no_newline():
    data = "x,y,z"
    f = io.StringIO(data)
    result = list(CustomCsvReader(f))

    assert result == [["x", "y", "z"]]
