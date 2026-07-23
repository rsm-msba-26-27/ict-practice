#!/usr/bin/env bash
# check-setup.sh — verify the RSM-MSBA environment is fully set up.
# Run from anywhere inside the cloned ict-practice folder:   ./check-setup.sh
# Every line should be a green check. Anything red: raise your hand.

pass=0; fail=0

ok()   { printf '  \033[32m[ OK ]\033[0m %s\n' "$1"; pass=$((pass+1)); }
bad()  { printf '  \033[31m[FAIL]\033[0m %s\n' "$1"; fail=$((fail+1)); }

echo
echo "RSM-MSBA setup check"
echo "--------------------"

# 1. direnv put the RSM environment on PATH
if [ -n "${RSM_WORKSPACE:-}" ]; then
  ok "RSM environment active (workspace: $RSM_WORKSPACE)"
else
  bad "RSM environment not active — are you inside ~/rsm-msba? (direnv should load it)"
fi

# 2. python is the shared nix-uv interpreter
pybin="$(command -v python || true)"
case "$pybin" in
  *".rsm-msba/envs/nix-uv"*) ok "python is the shared nix-uv environment" ;;
  "") bad "python not found on PATH" ;;
  *) bad "python resolves to $pybin (expected the nix-uv environment)" ;;
esac

# 3. python version
if pyver="$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))' 2>/dev/null)"; then
  ok "python $pyver runs"
else
  bad "python failed to run"
fi

# 4. quarto available
if qver="$(quarto --version 2>/dev/null)"; then
  ok "quarto $qver"
else
  bad "quarto not found"
fi

# 5. uv available
if uvver="$(uv --version 2>/dev/null)"; then
  ok "$uvver"
else
  bad "uv not found"
fi

# 6. git identity configured (rsm-github does this)
gname="$(git config user.name || true)"
gmail="$(git config user.email || true)"
if [ -n "$gname" ] && [ -n "$gmail" ]; then
  ok "git identity: $gname <$gmail>"
else
  bad "git identity not set — run rsm-github"
fi

# 7. GitHub SSH access (rsm-github + the key you added on github.com)
sshout="$(ssh -T -o BatchMode=yes -o ConnectTimeout=8 git@github.com 2>&1 || true)"
case "$sshout" in
  *"successfully authenticated"*) ok "GitHub SSH works (${sshout%%!*})" ;;
  *) bad "GitHub SSH failed — run rsm-github and add the key at github.com/settings/ssh/new" ;;
esac

# 8. this folder is a git clone of ict-practice
origin="$(git -C "$(dirname "$0")" remote get-url origin 2>/dev/null || true)"
case "$origin" in
  *ict-practice*) ok "you are inside a clone of ict-practice" ;;
  *) bad "run this from inside the cloned ict-practice folder" ;;
esac

# 9. PostgreSQL port assigned (module 06)
if [ -n "${PGPORT:-}" ]; then
  ok "PostgreSQL port assigned (PGPORT=$PGPORT)"
else
  bad "PGPORT not set — the environment did not load fully"
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "All $pass checks passed. Your setup is complete — on to the hunt."
else
  echo "$pass passed, $fail FAILED. Raise your hand and we will sort it out."
  exit 1
fi
