# A taco database with DuckDB

Two CSVs of San Diego taco-truck data — small enough to ship, too big to
eyeball:

- `trucks.csv` — 8 food trucks (id, name, neighborhood)
- `sales.csv` — ~600 daily sales rows (date, truck, item, quantity, price)

Used in Practice 01, Part E. The short version:

```bash
cd ~/rsm-msba/ict-practice/duckdb

# 1. put the CSVs into a database (one file: tacos.duckdb)
duckdb tacos.duckdb -c "CREATE TABLE trucks AS SELECT * FROM read_csv_auto('trucks.csv'); CREATE TABLE sales AS SELECT * FROM read_csv_auto('sales.csv');"

# 2. ask a question with SQL
duckdb tacos.duckdb -c "SELECT item, SUM(quantity) AS sold FROM sales GROUP BY item ORDER BY sold DESC;"

# 3. get the same answers BOTH ways — SQL and base Python — printed to compare
python explore.py
```

`tacos.duckdb` is a build artifact — it is git-ignored, so rebuild it any time
by re-running step 1.
