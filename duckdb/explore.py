# explore.py — answer the same three taco questions TWO ways and compare:
#   (1) with SQL, run from Python against the DuckDB database
#   (2) with base Python: dictionaries, loops, and if/else over the CSVs
# The point is to see that both give the same answers.
#
# Build the database first (Part E of the module, or the one-liner below), then:
#   python explore.py
#
#   duckdb tacos.duckdb -c "CREATE TABLE trucks AS SELECT * FROM read_csv_auto('trucks.csv'); CREATE TABLE sales AS SELECT * FROM read_csv_auto('sales.csv');"

import csv
import sys
from pathlib import Path

import duckdb

HERE = Path(__file__).parent
DB = HERE / "tacos.duckdb"
if not DB.exists():
    print(f"No database yet at {DB}.")
    print("Build it first (see Part E of the module), then run this again.")
    sys.exit(1)

# The database, for the SQL answers.
con = duckdb.connect(str(DB), read_only=True)

# The raw CSVs, for the base-Python answers (one dict per row, keyed by column).
with open(HERE / "trucks.csv") as f:
    trucks = list(csv.DictReader(f))
with open(HERE / "sales.csv") as f:
    sales = list(csv.DictReader(f))

# A JOIN is just a lookup table: a sale's truck_id tells us the truck's
# neighborhood and name. Build these once from trucks.csv.
neighborhood_of = {}
name_of = {}
for t in trucks:
    neighborhood_of[t["truck_id"]] = t["neighborhood"]
    name_of[t["truck_id"]] = t["name"]


def compare(title, sql, python_rows):
    """Print the SQL result and the base-Python result so they can be compared."""
    print(f"\n=== {title} ===")
    print("  -- SQL --")
    for row in con.execute(sql).fetchall():
        print("    " + "  ".join(str(value) for value in row))
    print("  -- base Python --")
    for row in python_rows:
        print("    " + "  ".join(str(value) for value in row))


# --- Q1: tacos sold per neighborhood ----------------------------------------
# A GROUP BY is a dictionary keyed by the group. The if/else asks: seen this
# neighborhood before? add to its total, else start a new one.
tacos_by_hood = {}
for s in sales:
    hood = neighborhood_of[s["truck_id"]]      # the "join"
    qty = int(s["quantity"])
    if hood in tacos_by_hood:
        tacos_by_hood[hood] = tacos_by_hood[hood] + qty
    else:
        tacos_by_hood[hood] = qty

compare(
    "Tacos sold per neighborhood (busiest first)",
    """
    SELECT t.neighborhood, SUM(s.quantity) AS tacos
    FROM sales s
    JOIN trucks t ON s.truck_id = t.truck_id
    GROUP BY t.neighborhood
    ORDER BY tacos DESC
    """,
    sorted(tacos_by_hood.items(), key=lambda kv: -kv[1]),   # ORDER BY ... DESC
)

# --- Q2: best-selling item overall ------------------------------------------
sold_by_item = {}
for s in sales:
    item = s["item"]
    qty = int(s["quantity"])
    if item in sold_by_item:
        sold_by_item[item] = sold_by_item[item] + qty
    else:
        sold_by_item[item] = qty

compare(
    "Best-selling item overall",
    """
    SELECT item, SUM(quantity) AS sold
    FROM sales
    GROUP BY item
    ORDER BY sold DESC
    """,
    sorted(sold_by_item.items(), key=lambda kv: -kv[1]),
)

# --- Q3: top 3 trucks by revenue --------------------------------------------
# revenue = quantity * price, totalled per truck. ORDER BY ... DESC is sorted
# with reverse=True; LIMIT 3 is the list slice [:3].
revenue_by_truck = {}
for s in sales:
    tid = s["truck_id"]
    revenue = int(s["quantity"]) * float(s["price"])
    if tid in revenue_by_truck:
        revenue_by_truck[tid] = revenue_by_truck[tid] + revenue
    else:
        revenue_by_truck[tid] = revenue

ranked = sorted(revenue_by_truck.items(), key=lambda kv: kv[1], reverse=True)

compare(
    "Top 3 trucks by revenue",
    """
    SELECT t.name, ROUND(SUM(s.quantity * s.price), 2) AS revenue
    FROM sales s
    JOIN trucks t ON s.truck_id = t.truck_id
    GROUP BY t.name
    ORDER BY revenue DESC
    LIMIT 3
    """,
    [(name_of[tid], round(revenue, 2)) for tid, revenue in ranked[:3]],
)

con.close()
