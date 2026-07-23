"""Validation tests for language-agnostic exploration fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SPECS_DIR = ROOT / "exploration"
FIXTURES_DIR = SPECS_DIR / "fixtures"
SCHEMAS_DIR = SPECS_DIR / "schemas"
FIXTURE_SCHEMA_PATH = SCHEMAS_DIR / "fixture.schema.json"
ENGINE_SCHEMAS_DIR = ROOT / "engine" / "schemas"
GAME_STATE_SCHEMA_PATH = ENGINE_SCHEMAS_DIR / "game-state.schema.json"
MATCH_STATE_SCHEMA_PATH = ENGINE_SCHEMAS_DIR / "match-state.schema.json"


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
def game_state_schema() -> dict:
    return _load_json(GAME_STATE_SCHEMA_PATH)


@pytest.fixture(scope="module")
def match_state_schema() -> dict:
    return _load_json(MATCH_STATE_SCHEMA_PATH)


@pytest.fixture(scope="module")
def schema_registry(
    game_state_schema: dict,
    match_state_schema: dict,
) -> Registry:
    return Registry().with_resources(
        (
            (schema["$id"], Resource.from_contents(schema))
            for schema in (game_state_schema, match_state_schema)
        )
    )


@pytest.fixture(scope="module")
def fixture_validator(
    fixture_schema: dict,
    schema_registry: Registry,
) -> Draft202012Validator:
    return Draft202012Validator(fixture_schema, registry=schema_registry)


@pytest.fixture(scope="module")
def match_state_validator(
    match_state_schema: dict,
    schema_registry: Registry,
) -> Draft202012Validator:
    return Draft202012Validator(match_state_schema, registry=schema_registry)


def test_schemas_are_valid(
    fixture_schema: dict,
    game_state_schema: dict,
    match_state_schema: dict,
):
    Draft202012Validator.check_schema(fixture_schema)
    Draft202012Validator.check_schema(game_state_schema)
    Draft202012Validator.check_schema(match_state_schema)


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
def test_base_state_matches_match_state_schema(
    fixture_path: Path,
    match_state_validator: Draft202012Validator,
):
    fixture = _load_json(fixture_path)
    errors = sorted(
        match_state_validator.iter_errors(fixture["spec"]["base_state"]), key=str
    )
    assert errors == [], "\n".join(
        f"{fixture_path}: base_state: "
        f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
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
    assert fixture["fixture_version"] == "exploration-fixture/v1"


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_directory_is_known_aspect(fixture_path: Path):
    fixture = _load_json(fixture_path)
    known_aspects = {
        path.stem
        for path in (SPECS_DIR / "aspects").glob("*.md")
        if path.stem != "TEMPLATE"
    }
    assert fixture["id"].split("/", 1)[0] in known_aspects


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_has_exactly_one_expected_outcome(fixture_path: Path):
    fixture = _load_json(fixture_path)
    has_state = "expect_resolved_state" in fixture
    has_error = "expect_error" in fixture
    assert has_state != has_error


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_base_state_card_ids_are_unique_when_hand_present(fixture_path: Path):
    fixture = _load_json(fixture_path)
    current_hand = fixture["spec"]["base_state"].get("current_hand")
    if current_hand is None:
        return

    seen_card_ids: set[str] = set()
    for cards in current_hand["state"]["hands"].values():
        for card in cards:
            card_id = card["id"]
            assert card_id not in seen_card_ids
            seen_card_ids.add(card_id)
