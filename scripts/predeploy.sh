#!/usr/bin/env bash
set -euo pipefail

# -------- settings --------
PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PKG="${PKG:-UARecords}"
TESTS="${TESTS:-tests}"
STUBS_DIR="${STUBS_DIR:-$PROJECT_ROOT/stubs}"
PYTHON="${PYTHON:-python3}"
COV_MIN="${COV_MIN:-85}"
FIX="${FIX:-0}"

section() { echo -e "\n\033[1;34m▶ $*\033[0m"; }
die() { echo "ERROR: $*" >&2; exit 1; }
ensure_module() {
  local mod="${1}"; local pkg="${2:-$1}"
  "$PYTHON" -c "import ${mod}" >/dev/null 2>&1 || {
    section "Installing '${pkg}' (user scope)"
    "$PYTHON" -m pip install --user "${pkg}" >/dev/null
  }
}

export PATH="$HOME/.local/bin:$PATH"
cd "$PROJECT_ROOT"

if command -v git >/dev/null 2>&1; then
  if ! git -c core.safecrlf=false diff --quiet || ! git diff --cached --quiet; then
    echo "WARNING: git working tree is dirty. Consider committing before predeploy." >&2
  fi
fi

[ -d "$STUBS_DIR" ] || die "STUBS_DIR does not exist: $STUBS_DIR"
"$PYTHON" -m pip --version >/dev/null 2>&1 || die "pip not available for $PYTHON"

# -------- bootstrap tools --------
ensure_module coverage
ensure_module build
ensure_module twine
ensure_module pytest
ensure_module black
ensure_module isort
ensure_module pylint
ensure_module mypy

HAS_PIP_AUDIT=0
if "$PYTHON" -c "import pip_audit" >/dev/null 2>&1; then HAS_PIP_AUDIT=1; else echo "NOTE: pip-audit not installed; skipping dependency audit"; fi

export MYPYPATH="${MYPYPATH:-$STUBS_DIR}"
export PYTHONPATH="$PROJECT_ROOT"

# -------- discover targets --------
SRC_TARGETS=()
[ -d "$PKG" ] && SRC_TARGETS+=("$PKG")
[ -d "$TESTS" ] && SRC_TARGETS+=("$TESTS")
while IFS= read -r -d '' py; do
  SRC_TARGETS+=("${py#./}")
done < <(find . -maxdepth 1 -type f -name '*.py' -print0)

# -------- clean --------
section "Clean caches"
find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
rm -rf .mypy_cache .pytest_cache .pylint.d .ruff_cache .coverage htmlcov dist build coverage.xml || true

# -------- formatting --------
if ((${#SRC_TARGETS[@]})); then
  if [ "$FIX" = "1" ]; then
    section "Black (format)"
    "$PYTHON" -m black "${SRC_TARGETS[@]}"
    section "isort (format)"
    "$PYTHON" -m isort "${SRC_TARGETS[@]}"
  else
    section "Black (check)"
    "$PYTHON" -m black --check "${SRC_TARGETS[@]}"
    section "isort (check)"
    "$PYTHON" -m isort --check-only "${SRC_TARGETS[@]}"
  fi
else
  echo "No sources found for formatting (skipping black/isort)."
fi

# -------- lint --------
section "Pylint"
PY_FILES=()
while IFS= read -r -d '' f; do PY_FILES+=("${f#./}"); done < <(find "$PKG" "$TESTS" . -type f -name '*.py' 2>/dev/null -print0 || true)
if ((${#PY_FILES[@]})); then
  "$PYTHON" -m pylint --rcfile=.pylintrc "${PY_FILES[@]}"
else
  echo "No Python files to lint; skipping."
fi

# -------- mypy --------
section "mypy"
"$PYTHON" -m mypy --config-file=mypy.ini .

# -------- tests & coverage --------
section "pytest with coverage"
if [ -d "$TESTS" ]; then
  "$PYTHON" -m coverage run -m pytest "$TESTS"
else
  echo "Tests directory '$TESTS' not found; running empty coverage session."
  "$PYTHON" -m coverage run - <<'PY'
# no tests — create empty .coverage
PY
fi
"$PYTHON" -m coverage report -m
TOTAL=$("$PYTHON" -m coverage report | awk 'END{print $NF}' | tr -d '%')
TOTAL=${TOTAL%%.*}
if [ -n "${TOTAL:-}" ] && [ "$TOTAL" -lt "$COV_MIN" ]; then
  die "coverage ${TOTAL}% is below minimum ${COV_MIN}%"
fi
"$PYTHON" -m coverage xml -o coverage.xml >/dev/null 2>&1 || true
"$PYTHON" -m coverage html -d htmlcov >/dev/null 2>&1 || true

# -------- build artifacts (optional) --------
if [ -f pyproject.toml ] || [ -f setup.cfg ] || [ -f setup.py ]; then
  section "Build sdist & wheel"
  "$PYTHON" -m build
  section "Twine check"
  "$PYTHON" -m twine check dist/*
else
  echo "No build config (pyproject.toml/setup.cfg/setup.py); skipping build & twine check."
fi

# -------- dependency audit (optional) --------
if [ "$HAS_PIP_AUDIT" -eq 1 ]; then
  section "pip-audit (advisory)"
  "$PYTHON" -m pip_audit || echo "pip-audit found advisories (review above)."
fi

section "Predeploy passed ✅"
echo "Done. To upload (if built): $PYTHON -m twine upload dist/*"