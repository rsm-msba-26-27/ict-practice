# explore.py — ask the taco database questions with SQL, from Python.
#
# Build the database first (Part E of the module, or the one-liner below), then:
#   python explore.py
#
#   duckdb tacos.duckdb -c "CREATE TABLE trucks AS SELECT * FROM read_csv_auto('trucks.csv'); CREATE TABLE sales AS SELECT * FROM read_csv_auto('sales.csv');"

import sys
from pathlib import Path

import duckdb

DB = Path(__file__).parent / "tacos.duckdb"
if not DB.exists():
    print(f"No database yet at {DB}.")
    print("Build it first (see Part E of the module), then run this again.")
    sys.exit(1)

con = duckdb.connect(str(DB), read_only=True)


def show(title, sql):
    """Run a query and print each row. fetchall() returns plain tuples."""
    print(f"\n{title}")
    for row in con.execute(sql).fetchall():
        print("  " + "  ".join(str(value) for value in row))


show("Tacos sold per neighborhood (busiest first)", """
    SELECT t.neighborhood, SUM(s.quantity) AS tacos
    FROM sales s
    JOIN trucks t ON s.truck_id = t.truck_id
    GROUP BY t.neighborhood
    ORDER BY tacos DESC
""")

show("Best-selling item overall", """
    SELECT item, SUM(quantity) AS sold
    FROM sales
    GROUP BY item
    ORDER BY sold DESC
""")

show("Top 3 trucks by revenue", """
    SELECT t.name, ROUND(SUM(s.quantity * s.price), 2) AS revenue
    FROM sales s
    JOIN trucks t ON s.truck_id = t.truck_id
    GROUP BY t.name
    ORDER BY revenue DESC
    LIMIT 3
""")

con.close()
