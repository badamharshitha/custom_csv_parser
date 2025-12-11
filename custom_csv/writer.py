from typing import TextIO, Iterable, Sequence


def _needs_quote(field: str, delim: str) -> bool:
    """Return True if field needs quoting (delimiter, newline or quote)."""
    if field == "":
        return False
    return any(c in field for c in (delim, "\n", "\r", '"'))


class CustomCsvWriter:
    """
    Minimal CSV writer.

    Automatically quotes fields containing delimiter, newline or quotes.
    Use writer.writerow(row) or writer.writerows(rows).
    """

    def __init__(
        self,
        fileobj: TextIO,
        delimiter: str = ",",
        newline: str = "\n",
    ):
        self.f = fileobj
        self.delim = delimiter
        self.newline = newline

    def _quote_field(self, field: str) -> str:
        if '"' in field:
            field = field.replace('"', '""')
        if _needs_quote(field, self.delim):
            return f'"{field}"'
        return field

    def writerow(self, row: Sequence[str]) -> None:
        out_fields = []
        for v in row:
            val = "" if v is None else str(v)
            out_fields.append(self._quote_field(val))
        self.f.write(self.delim.join(out_fields) + self.newline)

    def writerows(self, rows: Iterable[Sequence[str]]) -> None:
        for r in rows:
            self.writerow(r)


def dump(
    rows,
    fileobj: TextIO,
    delimiter: str = ",",
    newline: str = "\n",
):
    """Write multiple rows into a CSV file."""
    w = CustomCsvWriter(fileobj, delimiter=delimiter, newline=newline)
    w.writerows(rows)


def dumps(
    rows,
    delimiter: str = ",",
    newline: str = "\n",
) -> str:
    """Return CSV string from a list of rows."""
    from io import StringIO

    buf = StringIO()
    dump(rows, buf, delimiter=delimiter, newline=newline)
    return buf.getvalue()
