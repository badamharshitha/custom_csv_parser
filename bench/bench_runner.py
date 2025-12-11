import time
import csv
import pandas as pd
from custom_csv.reader import CustomCsvReader
from custom_csv.writer import CustomCsvWriter


def generate_data(rows: int, cols: int = 5):
    """Generate synthetic CSV rows."""
    base = []
    for i in range(rows):
        base.append([f"value_{i}_{c}" for c in range(cols)])
    return base


def time_write_custom(path, rows):
    start = time.time()
    with open(path, "w", encoding="utf-8") as f:
        w = CustomCsvWriter(f)
        w.writerows(rows)
    return time.time() - start


def time_write_std(path, rows):
    start = time.time()
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerows(rows)
    return time.time() - start


def time_read_custom(path):
    start = time.time()
    with open(path, "r", encoding="utf-8") as f:
        for _ in CustomCsvReader(f):
            pass
    return time.time() - start


def time_read_std(path):
    start = time.time()
    with open(path, "r", encoding="utf-8") as f:
        for _ in csv.reader(f):
            pass
    return time.time() - start


def main():
    sizes = [
        ("small", 100),
        ("medium", 1000),
        ("large", 5000),
        ("xlarge", 10000),  # REQUIRED BY ASSIGNMENT
    ]

    results = []

    for name, rows_count in sizes:
        rows = generate_data(rows_count)

        path_custom = f"bench/{name}_custom.csv"
        path_std = f"bench/{name}_std.csv"

        write_custom = time_write_custom(path_custom, rows)
        write_std = time_write_std(path_std, rows)

        read_custom = time_read_custom(path_custom)
        read_std = time_read_std(path_std)

        results.append(
            {
                "size": name,
                "rows": rows_count,
                "write_custom_s": write_custom,
                "write_std_s": write_std,
                "read_custom_s": read_custom,
                "read_std_s": read_std,
                "write_ratio_custom_vs_std": write_custom / write_std,
                "read_ratio_custom_vs_std": read_custom / read_std,
            }
        )

    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    df.to_csv("bench/results.csv", index=False)
    print("\nSaved benchmark results to bench/results.csv")


if __name__ == "__main__":
    main()
