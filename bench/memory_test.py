from custom_csv.reader import CustomCsvReader
from custom_csv.writer import CustomCsvWriter
import io


# --- Create a large CSV file on disk to test streaming ---
path = "bench/large_test.csv"

with open(path, "w", encoding="utf-8", newline="") as f:
    # write header
    f.write("c1,c2,c3,c4,c5\n")
    # write 200k rows
    for _ in range(200000):
        f.write("aaaaa,bbbbb,ccccc,ddddd,eeeee\n")

print("Large CSV written to:", path)


# --- Streaming read test (should not consume large RAM) ---
count = 0
with open(path, "r", encoding="utf-8", newline="") as f:
    reader = CustomCsvReader(f)
    for row in reader:
        count += 1

print("Rows read:", count)
