# plot_sales.py — bar chart of tacos sold per shop.
# Expects the sales CSVs in a `data/` folder next to this script.
import csv
from collections import Counter
from pathlib import Path

totals = Counter()
for path in sorted(Path("data").glob("sales_*.csv")):
    with open(path) as f:
        for row in csv.DictReader(f):
            totals[row["shop"]] += int(row["tacos_sold"])

width = max(len(s) for s in totals)
for shop, n in totals.most_common():
    print(f"{shop:<{width}}  {'#' * (n // 40)}  {n}")
