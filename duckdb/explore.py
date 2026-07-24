# explore.py — the same three questions as the SQL in Part E, answered with
# base Python: read the CSVs with the built-in csv module, then group, join, and
# total using dictionaries, loops, and if/else. No database, no extra packages.
#
#   python explore.py

import csv
from pathlib import Path

HERE = Path(__file__).parent

# Read both files into lists of dicts (one dict per row, keyed by column name).
with open(HERE / "trucks.csv") as f:
    trucks = list(csv.DictReader(f))
with open(HERE / "sales.csv") as f:
    sales = list(csv.DictReader(f))

# A JOIN is just a lookup table. Build these once from trucks.csv, then a sale's
# truck_id tells us the neighborhood and truck name.
neighborhood_of = {}
name_of = {}
for t in trucks:
    neighborhood_of[t["truck_id"]] = t["neighborhood"]
    name_of[t["truck_id"]] = t["name"]

# --- Tacos sold per neighborhood --------------------------------------------
# A GROUP BY is a dictionary keyed by the group. The if/else asks: have we seen
# this neighborhood before? Add to its total, or start a new one.
tacos_by_hood = {}
for s in sales:
    hood = neighborhood_of[s["truck_id"]]      # the "join"
    qty = int(s["quantity"])
    if hood in tacos_by_hood:
        tacos_by_hood[hood] = tacos_by_hood[hood] + qty
    else:
        tacos_by_hood[hood] = qty

print("Tacos sold per neighborhood (busiest first)")
for hood, tacos in sorted(tacos_by_hood.items(), key=lambda kv: -kv[1]):
    print(f"  {hood:<14} {tacos}")

# --- Best-selling item overall ----------------------------------------------
sold_by_item = {}
for s in sales:
    item = s["item"]
    qty = int(s["quantity"])
    if item in sold_by_item:
        sold_by_item[item] = sold_by_item[item] + qty
    else:
        sold_by_item[item] = qty

print("\nBest-selling item overall")
for item, sold in sorted(sold_by_item.items(), key=lambda kv: -kv[1]):
    print(f"  {item:<12} {sold}")

# --- Top 3 trucks by revenue ------------------------------------------------
# revenue = quantity * price, totalled per truck. ORDER BY ... DESC is sorted()
# with reverse=True; LIMIT 3 is the list slice [:3].
revenue_by_truck = {}
for s in sales:
    tid = s["truck_id"]
    revenue = int(s["quantity"]) * float(s["price"])
    if tid in revenue_by_truck:
        revenue_by_truck[tid] = revenue_by_truck[tid] + revenue
    else:
        revenue_by_truck[tid] = revenue

print("\nTop 3 trucks by revenue")
ranked = sorted(revenue_by_truck.items(), key=lambda kv: kv[1], reverse=True)
for tid, revenue in ranked[:3]:
    print(f"  {name_of[tid]:<18} {round(revenue, 2)}")
