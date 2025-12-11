# custom_csv

Small custom CSV reader & writer implementing basic RFC-style quoting and a small state-machine parser.

## Quickstart

1. Activate venv:
   Windows: `venv\Scripts\activate`

2. Run example:
   `python run.py`

3. Run tests:
   `python -m pytest -q`

4. Install editable (optional):
   `pip install -e .`

## API

- `CustomCsvReader(fileobj, delimiter=',')` — iterate to get rows (lists of strings).
- `CustomCsvWriter(fileobj, delimiter=',')` — `.writerow()` / `.writerows()`.
- `dumps(rows)` / `dump(rows, fileobj)` — convenience helpers.

## Design notes

Parser uses a 3-state machine: `FIELD`, `QUOTED`, `AFTER_QUOTE`. Supports:
- quoted fields containing delimiters and newlines
- double-quote escaping (`""` → `"`)
- tolerant handling of some malformed CSVs

## Development

- Tests: `pytest`
- Lint/format: `black`, `flake8`

## License
All rights reserved © 2025 B.N.S. Harshitha.

