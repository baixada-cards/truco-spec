"""Validation tests for language-agnostic notation fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SPECS_DIR = ROOT / "notation"
FIXTURES_DIR = SPECS_DIR / "fixtures"
SCHEMAS_DIR = SPECS_DIR / "schemas"
FIXTURE_SCHEMA_PATH = SCHEMAS_DIR / "fixture.schema.json"


def _load_json(path: Path) -> object:
    return json.loads(path.read_text())


def _fixture_paths() -> list[Path]:
    return sorted(FIXTURES_DIR.rglob("*.json"))


FIXTURE_PATHS = _fixture_paths()


def test_fixture_corpus_is_not_empty():
    assert FIXTURE_PATHS


@pytest.fixture(scope="module")
def fixture_schema() -> dict:
    return _load_json(FIXTURE_SCHEMA_PATH)


@pytest.fixture(scope="module")
def fixture_validator(fixture_schema: dict) -> Draft202012Validator:
    return Draft202012Validator(fixture_schema)


def test_schema_is_valid(fixture_schema: dict):
    Draft202012Validator.check_schema(fixture_schema)


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_parses_as_json(fixture_path: Path):
    _load_json(fixture_path)


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_matches_schema(
    fixture_path: Path,
    fixture_validator: Draft202012Validator,
):
    fixture = _load_json(fixture_path)
    errors = sorted(fixture_validator.iter_errors(fixture), key=str)
    assert errors == [], "\n".join(
        f"{fixture_path}: {'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in errors
    )


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_id_matches_relative_path(fixture_path: Path):
    fixture = _load_json(fixture_path)
    expected_id = fixture_path.relative_to(FIXTURES_DIR).with_suffix("").as_posix()
    assert fixture["id"] == expected_id


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_ruleset_is_current(fixture_path: Path):
    fixture = _load_json(fixture_path)
    assert fixture["ruleset"] == "truco-2p-v1"


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_format_is_current(fixture_path: Path):
    fixture = _load_json(fixture_path)
    assert fixture["fixture_version"] == "notation-fixture/v1"


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_directory_is_known_aspect(fixture_path: Path):
    fixture = _load_json(fixture_path)
    known_aspects = {path.stem for path in (SPECS_DIR / "aspects").glob("*.md")}
    assert fixture["id"].split("/", 1)[0] in known_aspects


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_has_exactly_one_expected_outcome(fixture_path: Path):
    fixture = _load_json(fixture_path)
    assert ("expect_fragment" in fixture) != ("expect_error" in fixture)
