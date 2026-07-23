"""Build the deterministic manifest for the public contract payload."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "spec-manifest.json"
PAYLOAD_PATHS = (
    Path("VERSION"),
    Path("rulesets"),
    Path("engine"),
    Path("exploration"),
    Path("notation"),
    Path("schemas"),
)
FIXTURE_FORMATS = {
    "engine": "engine-fixture/v1",
    "exploration": "exploration-fixture/v1",
    "notation": "notation-fixture/v1",
}


def _payload_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for relative_path in PAYLOAD_PATHS:
        path = root / relative_path
        if path.is_symlink():
            raise ValueError(f"payload path may not be a symlink: {relative_path}")
        if path.is_file():
            files.append(path)
            continue
        if not path.is_dir():
            raise FileNotFoundError(relative_path)
        files.extend(candidate for candidate in path.rglob("*") if candidate.is_file())
    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def _fixture_metadata(root: Path) -> tuple[dict[str, dict[str, Any]], list[str]]:
    corpora: dict[str, dict[str, Any]] = {}
    rulesets: set[str] = set()
    for surface in ("engine", "exploration", "notation"):
        fixture_paths = sorted((root / surface / "fixtures").rglob("*.json"))
        formats: set[str] = set()
        for path in fixture_paths:
            fixture = json.loads(path.read_text(encoding="utf-8"))
            rulesets.add(fixture["ruleset"])
            formats.add(fixture["fixture_version"])
        expected_format = FIXTURE_FORMATS[surface]
        if formats != {expected_format}:
            raise ValueError(
                f"{surface} fixture formats must be exactly {expected_format!r}: "
                f"{sorted(formats)!r}"
            )
        corpora[surface] = {
            "format": expected_format,
            "schema": f"{surface}/schemas/fixture.schema.json",
            "fixtures": f"{surface}/fixtures",
            "count": len(fixture_paths),
        }
    return corpora, sorted(rulesets)


def build_manifest(root: Path = ROOT) -> dict[str, Any]:
    """Return the canonical manifest as a JSON-serializable object."""

    corpora, ruleset_ids = _fixture_metadata(root)
    files = []
    for path in _payload_files(root):
        contents = path.read_bytes()
        files.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": len(contents),
                "sha256": hashlib.sha256(contents).hexdigest(),
            }
        )

    return {
        "$schema": "./schemas/spec-manifest.schema.json",
        "format": "truco-spec-manifest/v1",
        "version": (root / "VERSION").read_text(encoding="utf-8").strip(),
        "source": "https://github.com/baixada-cards/truco-spec",
        "rulesets": {
            ruleset_id: {"document": f"rulesets/{ruleset_id}.md"}
            for ruleset_id in ruleset_ids
        },
        "corpora": corpora,
        "files": files,
    }


def render_manifest(root: Path = ROOT) -> str:
    """Render the canonical manifest with stable whitespace and ordering."""

    return json.dumps(build_manifest(root), indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail instead of writing when manifest.json is stale",
    )
    args = parser.parse_args()
    rendered = render_manifest()

    if args.check:
        current = (
            MANIFEST_PATH.read_text(encoding="utf-8") if MANIFEST_PATH.exists() else ""
        )
        if current != rendered:
            print("spec-manifest.json is stale; run `make manifest`", file=sys.stderr)
            return 1
        return 0

    MANIFEST_PATH.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
