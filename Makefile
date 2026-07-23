.PHONY: check manifest release sync

sync:
	sfw uv sync --frozen --group dev

manifest:
	uv run --no-sync python scripts/build_manifest.py

release:
	uv run --no-sync python scripts/build_release.py

check:
	uv run --no-sync ruff format --check scripts tests
	uv run --no-sync ruff check scripts tests
	uv run --no-sync python -m pytest -q
	uv run --no-sync python scripts/build_manifest.py --check
