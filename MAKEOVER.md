# The messy folder makeover

`messy-project/` is what a project folder looks like after three "I'll clean it
up later" weeks: data, code, notes, images, and junk all dumped in one place.
Your job: impose order — using only the terminal.

## Step 0 — work on a COPY, outside this repo

Never reorganize inside someone else's repo. Copy the mess into your own
workspace first (note the `-r`: folders need *recursive* copy):

```bash
mkdir -p ~/rsm-msba/practice01
cp -r ~/rsm-msba/ict-practice/messy-project ~/rsm-msba/practice01/taco-cart
cd ~/rsm-msba/practice01/taco-cart
ls
```

## Step 1 — make a home for everything

```bash
mkdir data code docs figures
```

## Step 2 — move families of files with wildcards

`*.csv` means "every file ending in .csv" — one command moves them all:

```bash
mv *.csv data/
mv *.py *.ipynb code/
mv *.png figures/
mv *.md *.txt *.qmd docs/
```

Check your progress as you go: `ls`, or `lt` for the tree view.

## Step 3 — delete the junk

Some files should not be moved — they should not exist. Delete:

- `.DS_Store` (macOS clutter — hidden! `ls -a` shows it)
- `Untitled1.ipynb`, `Untitled7.ipynb` (empty notebooks; they went to `code/`)
- `temp.txt` (now in `docs/`)
- `sales_jan copy.csv` (a duplicate; now in `data/` — mind the space in the
  name: tab completion or quotes)

```bash
rm .DS_Store
rm "code/Untitled1.ipynb" code/Untitled7.ipynb docs/temp.txt
rm "data/sales_jan copy.csv"
```

## Step 4 — fix the worst file name in the world

```bash
mv "docs/final_report_v2_FINAL(3).qmd" docs/report.qmd
```

(`mv` renames when the target is a new name, moves when the target is a folder.)

## Step 5 — grade yourself

```bash
~/rsm-msba/ict-practice/check-structure.sh .
```

Every line green? Done. Something red? Fix it and run the check again.

## Bonus

The two scripts in `code/` expect the CSVs in `data/` — which is exactly where
you put them. From the folder root, run:

```bash
python code/clean_data.py
python code/plot_sales.py
```

Wait — `clean_data.py` works but looks for `data/` relative to where *you*
are standing, not where the script lives. Run it from inside `code/` and watch
it fail. That lesson is Practice 02, part B.
