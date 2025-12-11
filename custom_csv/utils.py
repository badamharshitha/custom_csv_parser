def needs_quote(field: str, delimiter: str) -> bool:
    """
    Check if a field requires quoting in CSV.
    Conditions:
    - contains delimiter (,)
    - contains newline (\n or \r)
    - contains quote (")
    """
    if field == "":
        return False

    return delimiter in field or "\n" in field or "\r" in field or '"' in field


def escape_quotes(field: str) -> str:
    """
    Escape quotes inside a CSV field by doubling them.
    Example:
        He said "ok"  ->  He said ""ok""
    """
    return field.replace('"', '""')
