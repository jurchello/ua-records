.PHONY: test lint format black isort check-all check-all-verbose help clean
SHELL := /bin/bash

PKG   := UARecords
TESTS := tests

help:
	@echo "Available targets:"
	@echo "  make test              - Run pytest test suite"
	@echo "  make lint              - Run pylint on source and tests"
	@echo "  make format            - Run black and isort (auto-format code)"
	@echo "  make black             - Run black only"
	@echo "  make isort             - Run isort only"
	@echo "  make clean             - Remove caches (__pycache__, .pytest_cache, etc.)"
	@echo "  make check-all         - Run clean, lint and test"
	@echo "  make check-all-verbose - Same as check-all but with verbose pylint"
	@echo "  make predeploy         - Run pre-deployment checks and formatting"
	@echo "  make predeploy-fix     - Run pre-deployment checks and formatting with auto-fixes"

test:
	pytest $(TESTS)

lint:
	@files="$$(find $(PKG) $(TESTS) -type f -name '*.py' 2>/dev/null)"; \
	if [[ -n "$$files" ]]; then \
	  echo "pylint on: $$files"; \
	  PYTHONPATH=$$(pwd) pylint --rcfile=.pylintrc $$files || true; \
	else \
	  echo "No Python files to lint in '$(PKG)' or '$(TESTS)'; skipping."; \
	fi

format:
	black $(PKG) $(TESTS) || true
	isort $(PKG) $(TESTS) || true

black:
	black $(PKG) $(TESTS) || true

isort:
	isort $(PKG) $(TESTS) || true

clean:
	@echo "Cleaning caches..."
	@find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .mypy_cache .pytest_cache .pylint.d .ruff_cache .coverage htmlcov || true

check-all: clean lint test

check-all-verbose: clean
	@echo ">>> LINT";   PYTHONPATH=$$(pwd) pylint --rcfile=.pylintrc $(PKG) $(TESTS) || true
	@echo ">>> MYPY";   mypy --config-file=mypy.ini .
	@echo ">>> TESTS";  pytest $(TESTS)

predeploy:
	scripts/predeploy.sh

predeploy-fix:
	@FIX=1 $(MAKE) predeploy