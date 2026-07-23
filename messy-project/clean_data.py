# clean_data.py — combine the monthly sales CSVs into one file.
# Expects the sales CSVs in a `data/` folder next to this script.
import csv
from pathlib import Path

rows = []
for path in sorted(Path("data").glob("sales_*.csv")):
    with open(path) as f:
        rows.extend(csv.DictReader(f))

out = Path("data") / "sales_all.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["date", "shop", "tacos_sold", "revenue"])
    w.writeheader()
    w.writerows(sorted(rows, key=lambda r: r["date"]))
print(f"wrote {out} ({len(rows)} rows)")
