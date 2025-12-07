#!/usr/bin/env bash
set -euo pipefail

# Activate virtual environment
# Works on Windows Git Bash / WSL paths; adjust if VENV changes
if [[ -f "venv/Scripts/activate" ]]; then
  # shellcheck disable=SC1091
  source "venv/Scripts/activate"
elif [[ -f "venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "venv/bin/activate"
else
  echo "Virtual environment not found. Expected venv/Scripts/activate or venv/bin/activate" >&2
  exit 1
fi

# Run pytest suite
python -m pytest -q tests/test_visualisation.py --disable-warnings

