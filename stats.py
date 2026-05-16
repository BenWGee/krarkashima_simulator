import csv
import statistics
from collections import Counter
import sys

INPUT_CSV = "results.csv"  # change if needed

def read_all_numeric_columns(path):
    cols = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for h in headers:
            cols[h] = []
        for row in reader:
            for h in headers:
                val = row.get(h, "").strip()
                if val == "":
                    continue
                try:
                    num = float(val) if ('.' in val or 'e' in val.lower()) else int(val)
                    cols[h].append(num)
                except ValueError:
                    # mark non-numeric by setting to None sentinel
                    cols[h] = None
        # remove non-numeric columns
        numeric = {h: v for h, v in cols.items() if v is not None}
    return numeric

def percentiles(data, ps=(25,50,75,90,95)):
    data_sorted = sorted(data)
    n = len(data_sorted)
    res = {}
    for p in ps:
        if n == 0:
            res[p] = None
            continue
        k = (p/100) * (n - 1)
        f = int(k)
        c = f + 1
        if c < n:
            val = data_sorted[f] + (k - f) * (data_sorted[c] - data_sorted[f])
        else:
            val = data_sorted[f]
        res[p] = val
    return res

def freq_table(data, top_n=10):
    c = Counter(data)
    return c.most_common(top_n)

def summarize(name, data):
    print(f"--- {name} ---")
    if not data:
        print("No numeric data found.\n")
        return
    n = len(data)
    print(f"Count: {n}")
    print(f"Mean: {statistics.mean(data):.6f}")
    print(f"Median: {statistics.median(data):.6f}")
    try:
        m = statistics.mode(data)
        print(f"Mode: {m}")
    except statistics.StatisticsError:
        counts = Counter(data)
        max_count = max(counts.values())
        modes = [k for k,v in counts.items() if v == max_count]
        print(f"Mode(s): {modes} (count={max_count})")
    if n > 1:
        print(f"Std dev (population): {statistics.pstdev(data):.6f}")
        print(f"Std dev (sample): {statistics.stdev(data):.6f}")
    print(f"Min: {min(data)}")
    print(f"Max: {max(data)}")
    p = percentiles(data)
    for key in (25,50,75,90,95):
        val = p[key]
        print(f"P{key}: {val:.6f}")
    print("Top frequencies:", freq_table(data, top_n=10))
    print()

def main():
    try:
        numeric_columns = read_all_numeric_columns(INPUT_CSV)
    except FileNotFoundError:
        print(f"File not found: {INPUT_CSV}", file=sys.stderr)
        sys.exit(1)
    if not numeric_columns:
        print("No numeric columns found in CSV.")
        return
    for col, data in numeric_columns.items():
        summarize(col, data)

if __name__ == "__main__":
    main()

