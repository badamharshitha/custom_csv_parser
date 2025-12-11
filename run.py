# run.py
from custom_csv.reader import CustomCsvReader
from custom_csv.writer import CustomCsvWriter
import io

data = [
    ["name", "comment"],
    ["Alice", "Hello, world"],
    ["Bob", "Line1\nLine2"],
    ["Eve", 'He said "hi"'],
]

buf = io.StringIO()
w = CustomCsvWriter(buf)
w.writerows(data)
csv_text = buf.getvalue()

print("CSV produced:")
print(csv_text)

# parse back
f = io.StringIO(csv_text)
r = CustomCsvReader(f)
for row in r:
    print("ROW:", row)
