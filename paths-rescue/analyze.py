# analyze.py — the San Diego Taco Awards.
#
# Reads data/menus.csv by RELATIVE path: this only works if your terminal is
# standing in the paths-rescue folder when you run it. That is the lesson.
#
#   cd ~/rsm-msba/ict-practice/paths-rescue
#   python analyze.py

import csv
import sys
from pathlib import Path

DATA = Path("data") / "menus.csv"

if not DATA.exists():
    print(f"FileNotFoundError is coming: '{DATA}' does not exist relative to")
    print(f"your current folder, which is: {Path.cwd()}")
    print()
    print("Fix: cd into the paths-rescue folder, then run:  python analyze.py")
    sys.exit(1)

with open(DATA) as f:
    rows = list(csv.DictReader(f))
for r in rows:
    r["price"] = float(r["price"])
    r["rating"] = float(r["rating"])
    r["salsa_heat"] = int(r["salsa_heat"])

print(f"Read {len(rows)} menu items from {len({r['shop'] for r in rows})} shops.\n")
print("=== The San Diego Taco Awards ===\n")

best = max(rows, key=lambda r: r["rating"])
print(f"Best taco in town   : {best['taco']} at {best['shop']} "
      f"({best['neighborhood']}) — rating {best['rating']}")

value = max(rows, key=lambda r: r["rating"] / r["price"])
print(f"Best value          : {value['taco']} at {value['shop']} — "
      f"rating {value['rating']} for ${value['price']:.2f}")

hottest = max(rows, key=lambda r: (r["salsa_heat"], r["rating"]))
print(f"Bravest salsa       : {hottest['shop']} ({hottest['taco']}, "
      f"heat {hottest['salsa_heat']}/5)")

hoods = {}
for r in rows:
    hoods.setdefault(r["neighborhood"], []).append(r["rating"])
top_hood = max(hoods, key=lambda h: sum(hoods[h]) / len(hoods[h]))
avg = sum(hoods[top_hood]) / len(hoods[top_hood])
print(f"Tastiest neighborhood: {top_hood} (average rating {avg:.2f})")
