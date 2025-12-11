import io
from custom_csv.reader import CustomCsvReader
from custom_csv.writer import CustomCsvWriter, dumps


def test_writer_basic():
    rows = [["a", "b", "c"], ["1", "2", "3"]]

    output = dumps(rows)
    f = io.StringIO(output)
    result = list(CustomCsvReader(f))

    assert result == rows


def test_writer_with_quotes_commas_newlines():
    rows = [["simple", "with,comma", 'has "quotes"', "multi\nline"]]

    output = dumps(rows)
    f = io.StringIO(output)
    parsed = list(CustomCsvReader(f))

    assert parsed == rows


def test_writer_fileobj(tmp_path):
    path = tmp_path / "test.csv"

    rows = [["a", "b,c", 'x"y']]

    with open(path, "w", newline="") as f:
        w = CustomCsvWriter(f)
        w.writerows(rows)

    with open(path, "r") as f:
        parsed = list(CustomCsvReader(f))

    assert parsed == rows
