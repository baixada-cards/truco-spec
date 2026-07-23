"""Repository-wide invariants for the public contract bundle."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_ROOTS = (
    ROOT / "rulesets",
    ROOT / "engine",
    ROOT / "exploration",
    ROOT / "notation",
    ROOT / "schemas",
)


def _payload_files() -> list[Path]:
    return sorted(
        (path for root in PAYLOAD_ROOTS for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def test_payload_has_no_symlinks() -> None:
    for root in PAYLOAD_ROOTS:
        assert not root.is_symlink()
        for path in root.rglob("*"):
            assert not path.is_symlink(), path.relative_to(ROOT)


def test_payload_paths_do_not_collide_case_insensitively() -> None:
    relative_paths = [path.relative_to(ROOT).as_posix() for path in _payload_files()]
    folded_paths = [path.casefold() for path in relative_paths]
    assert len(folded_paths) == len(set(folded_paths))


def test_text_payload_is_utf8_and_has_final_newline() -> None:
    for path in _payload_files():
        contents = path.read_bytes()
        text = contents.decode("utf-8")
        assert text.endswith("\n"), path.relative_to(ROOT)


def test_json_payload_rejects_duplicate_keys() -> None:
    paths = [*_payload_files(), ROOT / "spec-manifest.json"]
    for path in paths:
        if path.suffix != ".json":
            continue
        json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )


def test_schema_ids_are_canonical_and_unique() -> None:
    schema_paths = sorted(ROOT.rglob("*.schema.json"))
    schema_ids: list[str] = []
    for path in schema_paths:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        schema_id = schema.get("$id")
        assert isinstance(schema_id, str), path.relative_to(ROOT)
        assert schema_id.startswith("https://baixada.cards/spec/"), schema_id
        schema_ids.append(schema_id)
    assert len(schema_ids) == len(set(schema_ids))


def test_declared_ruleset_documents_exist() -> None:
    manifest = json.loads((ROOT / "spec-manifest.json").read_text(encoding="utf-8"))
    for ruleset in manifest["rulesets"].values():
        assert (ROOT / ruleset["document"]).is_file()
