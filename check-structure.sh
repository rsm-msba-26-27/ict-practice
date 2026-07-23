#!/usr/bin/env bash
# check-structure.sh — grade your messy-project makeover.
# Run it with the path to YOUR cleaned-up folder, e.g.:
#     ~/rsm-msba/ict-practice/check-structure.sh ~/rsm-msba/practice01/taco-cart
# or, from inside your cleaned folder:
#     ~/rsm-msba/ict-practice/check-structure.sh .

target="${1:-.}"
if [ ! -d "$target" ]; then
  echo "check-structure: '$target' is not a folder" >&2
  exit 2
fi
cd "$target" || exit 2

pass=0; fail=0
ok()  { printf '  \033[32m[ OK ]\033[0m %s\n' "$1"; pass=$((pass+1)); }
bad() { printf '  \033[31m[FIX ]\033[0m %s\n' "$1"; fail=$((fail+1)); }

echo
echo "Makeover check: $(pwd)"
echo "----------------------"

# The four folders exist
for d in data code docs figures; do
  if [ -d "$d" ]; then ok "folder $d/ exists"; else bad "missing folder: $d/"; fi
done

# Nothing loose in the root except the four folders (and hidden files)
loose="$(find . -maxdepth 1 -type f ! -name '.*' | sed 's|^\./||')"
if [ -z "$loose" ]; then
  ok "no loose files in the root"
else
  bad "still loose in the root: $(echo "$loose" | tr '\n' ' ')"
fi

# All CSVs live in data/
stray_csv="$(find . -name '*.csv' ! -path './data/*' | sed 's|^\./||')"
if [ -z "$stray_csv" ]; then ok "every .csv is in data/"; else bad "csv outside data/: $(echo "$stray_csv" | tr '\n' ' ')"; fi

# Scripts and notebooks live in code/
stray_code="$(find . \( -name '*.py' -o -name '*.ipynb' \) ! -path './code/*' | sed 's|^\./||')"
if [ -z "$stray_code" ]; then ok "every .py/.ipynb is in code/"; else bad "code outside code/: $(echo "$stray_code" | tr '\n' ' ')"; fi

# Images live in figures/
stray_img="$(find . -name '*.png' ! -path './figures/*' | sed 's|^\./||')"
if [ -z "$stray_img" ]; then ok "every .png is in figures/"; else bad "image outside figures/: $(echo "$stray_img" | tr '\n' ' ')"; fi

# Junk is gone
junk="$(find . \( -name '.DS_Store' -o -name 'Untitled*' -o -name '* copy*' -o -name 'temp.txt' \) | sed 's|^\./||')"
if [ -z "$junk" ]; then ok "junk files deleted"; else bad "junk still here: $(echo "$junk" | tr '\n' ' ')"; fi

# The FINAL(3) report got a sane name
if find . -name '*FINAL*' -o -name '*final_report_v2*' | grep -q .; then
  bad "rename the 'final_report_v2_FINAL(3).qmd' file to something sane (e.g. docs/report.qmd)"
else
  ok "no more _FINAL(3) file names"
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "All $pass checks passed — this folder is a pleasure to work in."
else
  echo "$pass passed, $fail to fix. Run me again after each fix."
  exit 1
fi
