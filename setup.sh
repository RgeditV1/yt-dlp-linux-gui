#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

# Bootstrap a local venv in `.venv` and install deps.
# Works on Linux/macOS and on Windows if executed from Git Bash/MSYS2.

PYTHON=()
if command -v python3 >/dev/null 2>&1; then
  PYTHON=(python3)
elif command -v python >/dev/null 2>&1; then
  PYTHON=(python)
elif command -v py >/dev/null 2>&1; then
  PYTHON=(py -3)
else
  echo "ERROR: Python not found (need python3/python/py)." >&2
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  "${PYTHON[@]}" -m venv .venv
fi

VENV_PY=""
if [[ -x ".venv/bin/python" ]]; then
  VENV_PY=".venv/bin/python"
elif [[ -x ".venv/Scripts/python.exe" ]]; then
  VENV_PY=".venv/Scripts/python.exe"
elif [[ -x ".venv/Scripts/python" ]]; then
  VENV_PY=".venv/Scripts/python"
else
  echo "ERROR: venv python not found under .venv/ (venv creation may have failed)." >&2
  exit 1
fi

"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install -r requirements.txt

echo "OK: venv ready."
