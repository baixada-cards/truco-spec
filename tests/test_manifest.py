"""Validation for the deterministic public payload manifest."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.build_manifest import build_manifest

ROOT = Path(__file__).resolve().parents[1]


def test_manifest_matches_payload() -> None:
    expected = build_manifest(ROOT)
    actual = json.loads((ROOT / "spec-manifest.json").read_text(encoding="utf-8"))
    assert actual == expected


def test_manifest_matches_schema() -> None:
    manifest = build_manifest(ROOT)
    schema = json.loads(
        (ROOT / "schemas/spec-manifest.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(manifest)


def test_manifest_paths_are_sorted_and_unique() -> None:
    manifest = build_manifest(ROOT)
    paths = [entry["path"] for entry in manifest["files"]]
    assert paths == sorted(set(paths))


def test_manifest_covers_every_fixture_surface() -> None:
    manifest = build_manifest(ROOT)
    assert manifest["corpora"] == {
        "engine": {
            "count": 67,
            "fixtures": "engine/fixtures",
            "format": "engine-fixture/v1",
            "schema": "engine/schemas/fixture.schema.json",
        },
        "exploration": {
            "count": 24,
            "fixtures": "exploration/fixtures",
            "format": "exploration-fixture/v1",
            "schema": "exploration/schemas/fixture.schema.json",
        },
        "notation": {
            "count": 36,
            "fixtures": "notation/fixtures",
            "format": "notation-fixture/v1",
            "schema": "notation/schemas/fixture.schema.json",
        },
    }
    assert manifest["rulesets"] == {
        "truco-2p-v1": {"document": "rulesets/truco-2p-v1.md"}
    }
