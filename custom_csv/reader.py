from typing import TextIO, List, Iterator


class CustomCsvReader:
    """
    Streaming CSV reader that yields one row at a time.

    Handles quoted fields, escaped quotes ("") and embedded newlines.
    """

    def __init__(self, fileobj: TextIO, delimiter: str = ","):
        self.f = fileobj
        self.delim = delimiter

    def __iter__(self) -> Iterator[List[str]]:
        FIELD = 0
        QUOTED = 1
        AFTER_QUOTE = 2

        state = FIELD
        field_chars: List[str] = []
        row: List[str] = []

        def end_field():
            nonlocal field_chars
            row.append("".join(field_chars))
            field_chars = []

        # Read one character at a time; keeps memory usage low.
        while True:
            ch = self.f.read(1)
            if ch == "":
                # EOF
                break

            if state == FIELD:
                if ch == self.delim:
                    end_field()
                elif ch == '"':
                    state = QUOTED
                elif ch == "\r":
                    # handle CRLF: peek next char
                    next_ch = self.f.read(1)
                    if next_ch not in ("\n", ""):
                        # try to push back if possible
                        try:
                            self.f.seek(self.f.tell() - 1)
                        except Exception:
                            pass
                    end_field()
                    yield row
                    row = []
                elif ch == "\n":
                    end_field()
                    yield row
                    row = []
                else:
                    field_chars.append(ch)

            elif state == QUOTED:
                if ch == '"':
                    state = AFTER_QUOTE
                else:
                    field_chars.append(ch)

            elif state == AFTER_QUOTE:
                if ch == '"':
                    # escaped quote -> append one quote and return to quoted
                    field_chars.append('"')
                    state = QUOTED
                elif ch == self.delim:
                    end_field()
                    state = FIELD
                elif ch == "\r":
                    next_ch = self.f.read(1)
                    if next_ch not in ("\n", ""):
                        try:
                            self.f.seek(self.f.tell() - 1)
                        except Exception:
                            pass
                    end_field()
                    yield row
                    row = []
                    state = FIELD
                elif ch == "\n":
                    end_field()
                    yield row
                    row = []
                    state = FIELD
                else:
                    # stray characters after closing quote: tolerant behavior
                    field_chars.append(ch)
                    state = FIELD

        # EOF finalization
        if state == QUOTED:
            # unterminated quoted field: accept what we have
            end_field()
            if row:
                yield row
        else:
            if state == AFTER_QUOTE:
                end_field()
            if field_chars:
                end_field()
            if row:
                yield row
